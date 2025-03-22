# Blackjack Battle (Controller)

A Blackjack game controller designed to be deployed as a Google Cloud Cloud Run service. Blackjack battle players are deployed alonside this controller to receive current game state and return a response. Templates for a player include relevant endpoints however the game logic is left to the developer to create.


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