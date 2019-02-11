# Group Flight Convergence
A program using genetic algorithm to solve optimization problem in choosing flights.

## Overview
Group flight convergence: a program using genetic algorithm to solve optimization problem in choosing flights for a group of people so that they arrive and depart a single destination with as little cost as possible.

## Requirement
You need to have Google API key to access QPX Express Airfare API. After getting the key, insert it into the code.

## Usage
1. In Python interactive session, run `from gfc import *`. 
2. Input required information. If you finish, type `y` and Enter; otherwise, just press Enter.
3. Run different functions:
  * `schedulecost(schedule)`: print finess value of a schedule
  * `printschedule(schedule)`: neatly print schedule table
  * `geneticoptimization(dom,schedulecost)`: apply genetic algorithm to choose the best flight schedule.
  * `geneticshake(dom,schedulecost)`: give several more iterations on `geneticoptimization()`

Inspired by "Programming Collective Intelligence" by Toby Segaran.
