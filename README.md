## Project Overview

Our project implements a multiplayer Tic Tac Toe game where two players can connect to a local server to play in real-time. This game leverages principles of data communication and client-server architecture, designed to support seamless data exchange and interaction over a local area network (LAN).

## Objectives

- Client-Server Architecture: The game logic is managed on the server, while each player connects as a client.
- Real-Time Data Exchange: Synchronizes game states and updates for both players instantly.
- User-Friendly Interface: Provides a clear, intuitive interface for an enjoyable experience.
- Network Efficiency: Uses efficient protocols to reduce latency.
- Error Handling: Incorporates robust error management to ensure smooth gameplay.

## Key Features

- Multiplayer Mode: Connects two players over LAN for competitive play.
Game State Synchronization: Both clients display the same game state consistently.
- In-Game Chat: Allows players to communicate during the game.
- Score Tracking: Tracks and displays players' scores across sessions.

## Protocols

- TCP (Transmission Control Protocol): Chosen for its reliability, TCP will ensure that all packets are received in order and without loss. This is essential for maintaining a consistent game state across both clients.

- JSON (or CSV, or XML): For clear and organized data transfer, JSON will be used to structure game states, messages, and scores, making it easy to parse and debug.

## Implementation Details

### Components
- Command-line Tic-Tac-Toe Mechanics (Python): Game logic implemented as a command-line interface.
- Client-Server Communication: The server listens for client connections, manages game states, and ensures message delivery.

### Error Handling
- Connection Loss: If a connection is dropped, the server attempts to reconnect.
- Invalid Moves: The server checks for valid moves, preventing players from making illegal moves.
