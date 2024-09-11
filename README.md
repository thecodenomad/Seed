# Seed

---

Seed is a snowflake type operation when it comes to writing. The idea is to start with a
asset (character or setting) and then add descriptors. A descriptor can be shared between
assets but are destinct from assets.

A seed grows much like a plant, and is meant to foster ideas in an organic fashion. This
should be taylored for the experience, but for now, the seed's rules follow that of
the Fibonacci sequence.

The idea is to take the assets and descriptors and use them as a seed that get's passed
into an AI model. The AI can then be asked specific prompts about an asset and/or
provide a summary for the asset based on the input.

# Level Up

---

The concept of Leveling Up is similar to an RPG. For the initial implementation, the
Leveling Up algorithm makes use of the Fibonacci sequence. This is meant to facilitate
organic growth.

TODO: Leveling Up should be abstracted so that other numerical sequences can be used.

## Global State

This holds the global state of assets and descriptors. When the number of assets or
descriptors reach a fibonacci number, the global asset or global descriptor will be set
to a Level Up status. The next fibonacci number is calculated to determine how many
assets/descriptors are needed for the next Level up.

## Asset State

An asset levels up when it's number of linked descriptors is equal to a Fibonacci number.

## Descriptor State

A descriptor levels up when it's number of descriptions is equal to a Fibonacci number.
NOTE: Descriptions themselves must have a word length equal to a Fibonacci number.

### Example of valid descriptions:

```
len("blue".split())
len("blue hair".split())
len("blue haired woman".split())
len("blue haired woman in bar".split())
len("blue haired woman in bar drinking a beer".split())
```

Examples of invalid descriptions:

```
len("blue haired emo woman".split())
len("blue haired emo woman in bar".split())
len("blue haired emo woman in bar drinking an alcoholic cocktail".split())
```

# Next Steps

---

These are the next planned features.

### Immediate Need

-   TODO: Export to JSON
-   TODO: Build a simple GTK GUI to capture Assets and Descriptors
-   TODO: Setup pytorch and interaction with a model.
-   TODO: Add the ability to pass in the lengths of the global objects as a part of the calculations

### Medium Term

-   TODO: Plugin to support descriptors as social media hashtags, and the description as
    any content associated with a post

### Longer Term

-   TODO: Automate how a model is added/downloaded into the project
-   TODO: Add 'type' category for the cacluation function used to determine leveling up
-   TODO: Abstract out calculations for Assets and descriptors allowing for much
    easier plugin/alternate level up function calculations.
