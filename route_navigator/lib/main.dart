// main.dart

import 'package:flutter/material.dart';
import 'package:flutter_typeahead/flutter_typeahead.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:latlong2/latlong.dart';
import 'package:flutter_map/flutter_map.dart';

void main() {
  runApp(const SafeRouteApp());
}

class SafeRouteApp extends StatelessWidget {
  const SafeRouteApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Safe Route Navigation',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const LocationInputScreen(),
    );
  }
}

class LocationInputScreen extends StatefulWidget {
  const LocationInputScreen({super.key});

  @override
  State<LocationInputScreen> createState() => _LocationInputScreenState();
}

class _LocationInputScreenState extends State<LocationInputScreen> {
  final TextEditingController sourceController = TextEditingController();
  final TextEditingController destinationController = TextEditingController();

  String? selectedSource;
  String? selectedDestination;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Safe Route Planner")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TypeAheadField<String>(
              textFieldConfiguration: TextFieldConfiguration(
                controller: sourceController,
                decoration: const InputDecoration(labelText: "Source Location"),
              ),
              suggestionsCallback: fetchSuggestions,
              itemBuilder: (context, suggestion) => ListTile(title: Text(suggestion)),
              onSuggestionSelected: (suggestion) {
                setState(() {
                  selectedSource = suggestion;
                  sourceController.text = suggestion;
                });
              },
            ),
            const SizedBox(height: 16),
            TypeAheadField<String>(
              textFieldConfiguration: TextFieldConfiguration(
                controller: destinationController,
                decoration: const InputDecoration(labelText: "Destination Location"),
              ),
              suggestionsCallback: fetchSuggestions,
              itemBuilder: (context, suggestion) => ListTile(title: Text(suggestion)),
              onSuggestionSelected: (suggestion) {
                setState(() {
                  selectedDestination = suggestion;
                  destinationController.text = suggestion;
                });
              },
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () {
                if (selectedSource != null && selectedDestination != null) {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => MapScreen(
                        source: selectedSource!,
                        destination: selectedDestination!,
                      ),
                    ),
                  );
                }
              },
              child: const Text("Find Safe Route"),
            ),
          ],
        ),
      ),
    );
  }

  Future<List<String>> fetchSuggestions(String query) async {
    final url = 'https://nominatim.openstreetmap.org/search?q=$query&format=json&limit=5';
    final response = await http.get(Uri.parse(url));
    final List data = jsonDecode(response.body);
    return data.map((e) => e['display_name'].toString()).toList();
  }
}

class MapScreen extends StatefulWidget {
  final String source;
  final String destination;

  const MapScreen({super.key, required this.source, required this.destination});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  final String openWeatherApiKey = '8987e6f85be22011a64f8bec37405da5'; // Replace this
  final String openRouteApiKey = '5b3ce3597851110001cf624862bbc70092534f50b7a8c112631db650';

  LatLng? sourceCoords;
  LatLng? destCoords;
  Map<String, dynamic>? sourceWeather;
  Map<String, dynamic>? destWeather;

  List<List<LatLng>> allRoutes = [];
  int bestRouteIndex = 0;

  @override
  void initState() {
    super.initState();
    fetchCoordinatesAndWeather().then((_) => fetchRoutesAndPickBest());
  }

  Future<void> fetchCoordinatesAndWeather() async {
    sourceCoords = await getCoordinatesFromAddress(widget.source);
    destCoords = await getCoordinatesFromAddress(widget.destination);

    sourceWeather = await fetchWeatherFromCoords(sourceCoords!);
    destWeather = await fetchWeatherFromCoords(destCoords!);

    setState(() {});
  }

  Future<LatLng> getCoordinatesFromAddress(String address) async {
    final url = 'https://nominatim.openstreetmap.org/search?q=$address&format=json&limit=1';
    final response = await http.get(Uri.parse(url));
    final data = jsonDecode(response.body);
    final lat = double.parse(data[0]['lat']);
    final lon = double.parse(data[0]['lon']);
    return LatLng(lat, lon);
  }

  Future<Map<String, dynamic>> fetchWeatherFromCoords(LatLng coords) async {
    final url =
        'https://api.openweathermap.org/data/2.5/weather?lat=${coords.latitude}&lon=${coords.longitude}&appid=$openWeatherApiKey&units=metric';
    final response = await http.get(Uri.parse(url));
    return jsonDecode(response.body);
  }

  Future<void> fetchRoutesAndPickBest() async {
    final url = Uri.parse('https://api.openrouteservice.org/v2/directions/driving-car/geojson');
    final headers = {
      'Authorization': openRouteApiKey,
      'Content-Type': 'application/json',
    };
    final body = jsonEncode({
      "coordinates": [
        [sourceCoords!.longitude, sourceCoords!.latitude],
        [destCoords!.longitude, destCoords!.latitude]
      ],
      "alternative_routes": {
        "target_count": 3,
        "share_factor": 0.6,
        "weight_factor": 1.4
      }
    });

    final response = await http.post(url, headers: headers, body: body);
    final data = jsonDecode(response.body);

    allRoutes.clear();
    List<double> scores = [];

    for (var feature in data['features']) {
      final coords = feature['geometry']['coordinates']
          .map<LatLng>((p) => LatLng(p[1], p[0]))
          .toList();

      allRoutes.add(coords);

      final midPoint = coords[(coords.length / 2).floor()];
      final weather = await fetchWeatherFromCoords(midPoint);

      final temp = weather['main']['temp'];
      final humidity = weather['main']['humidity'];
      final rain = weather['rain']?['1h'] ?? 0.0;
      final visibility = weather['visibility'] ?? 10000;

      final pollution = _mockAirQuality(midPoint);
      final flood = _mockFloodRisk(midPoint);

      double score = 0;
      score += (temp > 35 || temp < 0) ? 20 : 0;
      score += (humidity > 80) ? 10 : 0;
      score += (rain > 5) ? 15 : 0;
      score += (visibility < 1000) ? 10 : 0;
      score += pollution / 2;
      score += flood;

      scores.add(score);
    }

    bestRouteIndex = scores.indexOf(scores.reduce((a, b) => a < b ? a : b));
    setState(() {});
  }

  int _mockAirQuality(LatLng point) {
    return (point.latitude * point.longitude % 100).round();
  }

  int _mockFloodRisk(LatLng point) {
    return (point.latitude + point.longitude % 3).round();
  }

  @override
  Widget build(BuildContext context) {
    if (sourceCoords == null || destCoords == null || sourceWeather == null || destWeather == null) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    return Scaffold(
      appBar: AppBar(title: const Text("Safe Route Map")),
      body: Column(
        children: [
          Expanded(
            child: FlutterMap(
              options: MapOptions(
                initialCenter: sourceCoords!,
                initialZoom: 13.0,
              ),
              children: [
                TileLayer(
                  urlTemplate: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                  subdomains: ['a', 'b', 'c'],
                ),
                MarkerLayer(
                  markers: [
                    Marker(
                      point: sourceCoords!,
                      width: 80,
                      height: 80,
                      child: const Icon(Icons.location_pin, color: Colors.green, size: 40),
                    ),
                    Marker(
                      point: destCoords!,
                      width: 80,
                      height: 80,
                      child: const Icon(Icons.flag, color: Colors.blue, size: 40),
                    ),
                  ],
                ),
                PolylineLayer(
                  polylines: allRoutes.asMap().entries.map((entry) {
                    final index = entry.key;
                    final route = entry.value;
                    return Polyline(
                      points: route,
                      strokeWidth: 6.0,
                      color: index == bestRouteIndex ? Colors.green : Colors.red,
                    );
                  }).toList(),
                ),
              ],
            ),
          ),
          SafeRouteIndicator(isSafeRoute: true),
          weatherTile("Source Weather", sourceWeather!),
          weatherTile("Destination Weather", destWeather!),
        ],
      ),
    );
  }

  Widget weatherTile(String title, Map<String, dynamic> weather) {
    final condition = weather['weather'][0]['main'];
    final desc = weather['weather'][0]['description'];
    final temp = weather['main']['temp'];
    final humidity = weather['main']['humidity'];
    final iconCode = weather['weather'][0]['icon'];

    return Card(
      elevation: 3,
      margin: const EdgeInsets.all(8),
      child: ListTile(
        leading: Image.network('https://openweathermap.org/img/wn/$iconCode@2x.png'),
        title: Text(title),
        subtitle: Text("$condition ($desc)\nTemp: $temp°C, Humidity: $humidity%"),
      ),
    );
  }
}

class SafeRouteIndicator extends StatelessWidget {
  final bool isSafeRoute;

  const SafeRouteIndicator({super.key, required this.isSafeRoute});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Card(
        color: isSafeRoute ? Colors.green : Colors.red,
        child: Padding(
          padding: const EdgeInsets.all(12.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                isSafeRoute ? Icons.check_circle : Icons.cancel,
                color: Colors.white,
                size: 32.0,
              ),
              const SizedBox(width: 8),
              Text(
                isSafeRoute ? "This route is safe!" : "This route is unsafe.",
                style: const TextStyle(color: Colors.white, fontSize: 20),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
