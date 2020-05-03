# MyPlace

This problem is part of the `Intro to Hacking Workshop`. View the [Bug Bounty Guide](https://github.com/hackmtlca/bug-bounty-guide) for more information about the score system.

## Context

In 2005, [Samy Kamkar](https://en.wikipedia.org/wiki/Samy_Kamkar) created the fastest spreading [computer worm](https://en.wikipedia.org/wiki/Computer_worm) (There is a [short documentary here](https://www.youtube.com/watch?v=DtnuaHl378M)). He pioneered an attack that is still [very devastating today](https://owasp.org/www-project-top-ten/); Cross-Site Scripting (XSS). An XSS attack occurs when someone is capable of running code on another person's browser. If a person with bad intent gets a hold of this, they could steal credientals and essentially destroy websites. In the case of Samy Kamkar, he end up with millions of friends on [MySpace](https://myspace.com/). Your task is to replicate what Samy Kamkar has done previously using the new and improved `MyPlace`. The only difference now is that you're only affecting bot lives. The flag will be automatically displayed once you reach 75% of people - as default that is 38 people. Feel free to explore other solutions than XSS aswell. We hope that this real-life inspired example will make you understand the scale a cyberattack can reach. We also hope that this will also make your more prone to sanitize your inputs.

## Running the App

All you need is `Docker`. Run the following command in the root of this repository:

```
docker-compose up
```

A frontend instance will be created at `http://localhost/`. Note that the database is reset when the service is restarted.

## Closing the App

The app can be closed using CTRL+C. The app can be completely closed with the following command in the root of this repository:

```
docker-compose down
```

## Additional App Config

If you happen to have issues with Docker, `pip install` the `requirments.txt` from root. This will let you try out the website but you won't have access to the bots. 