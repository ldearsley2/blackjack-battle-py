# Blackjack Battle (Controller)

A Blackjack game controller designed to be deployed as a Google Cloud Run service. Blackjack battle players are deployed alongside the controller to receive current game state and return a response. Templates for a player include relevant endpoints however the game logic is left for the developer to create.


## Installation

Install blackjack battle with poetry

```bash
  poetry install
```
    
## Deployment

To deploy this project locally:

```bash
  poetry run dev
```