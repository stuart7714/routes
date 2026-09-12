# routes
An A* route finder in Python for programming practice

# Overview

The user is shown a hex map which is a grid of hexagons representing a 2-D plane. They can right click on a hex to place a yellow start point and then a red end point. When a start and end are placed then the shortest route is shown in orange.

The user may also click on hexes to fill them in and create barriers which the route must pass around.

# Code Structure

The route finding algorithm is [A*](https://en.wikipedia.org/wiki/A*_search_algorithm).

This algorithm is implemented in the `Map` class which contains the arrangement of hexes in the hex map. Each hex is an instance of the `Hex` class.

Each hex has a state:

- `EMPTY`: The hex contains nothing
- `BARRIER`: The hex is a barrier and a route cannot pass through
- `START`: The hex is a start location for a route
- `END`: The hex is an end location for a route