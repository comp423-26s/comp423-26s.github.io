---
code: RD10
title: Advancements in Communication between Computing Systems
date: 2026-01-23
due: 2026-01-27
type:  reading
threads: ["System / APIs"]
authors: [Kris Jordan]
---

# 2. Advancements in Communication between Computing Systems

As we turn our attention to communication between systems, that software engineers design and implement, it is helpful to have some historical context. Just as structured communication enables humans to align on shared goals, advances in computing systems have focused on making the exchange of information between machines more structured, scalable, and reliable. This history lays the foundation for understanding how modern APIs play a central role in today’s interconnected digital world.

## The Early Days: Batch Processing and Punch Cards
In the 1950s and 60s, computers were massive, room-sized machines, and communication with them was painstakingly slow. Users prepared instructions using punch cards—thin cardboard sheets with holes representing binary commands. The cards were fed into the computer in batches, and the machine would process them before producing an output, often printed on paper. 

While revolutionary at the time, this method lacked interactivity. Communication was strictly one-way, requiring users to wait for results before making adjustments.

## The Shift to Real-Time Interaction: Time-Sharing Systems

In the 1960s, time-sharing systems introduced real-time interaction with computers. This is when _shells_, like the command-line interfaces software engineers (and you, in 211 and this course!) still use today, rose in prominence.

These systems allowed multiple users to work on the same machine simultaneously via terminals. Communication became more dynamic, enabling developers to write, test, and debug programs interactively.

This period also saw the rise of early message-passing protocols, as systems began to share data across connected machines. However, these interactions were often bespoke and required deep technical knowledge, limiting their accessibility to a small group of experts. There were no standards for information exchange between two systems or programs.

## Networking Revolution: The ARPANET and Protocols

The creation of the ARPANET in 1969—a precursor to the internet—marked a significant milestone in system communication. For the first time, computers located miles apart could exchange data. Early protocols like NCP (Network Control Protocol) and later TCP/IP (Transmission Control Protocol/Internet Protocol) laid the groundwork for modern networking by standardizing how systems should format and transmit messages.

With standardized protocols, communication across systems became more predictable and scalable. These innovations enabled the development of distributed systems, where multiple computers could collaborate on a single task. It’s not unlike how the advent of telephone systems unlocked new forms of collaboration and communication among people.

## The Rise of the Web: HTTP and HTML
The invention of the World Wide Web in the 1990s transformed how systems—and people—interacted. HTTP (Hypertext Transfer Protocol) became the standard for requesting and transmitting resources over the web, while HTML (Hypertext Markup Language) provided a consistent way to display those resources.

This period also saw the emergence of APIs in their earliest forms. Web APIs allowed applications to request data or functionality from other services, albeit in a relatively unstructured and inconsistent manner compared to today.

## Modern APIs: REST and Beyond
In the early 2000s, REST (Representational State Transfer) emerged as a simpler, more flexible approach to API design. RESTful APIs leveraged familiar web methods, such as "retrieving" or "updating" resources, to create predictable and scalable communication between clients and servers.

Today, APIs are fundamental to how most modern web and mobile applications function. Applications are often split into at least two conceptual parts: the front-end, which is what users interact with, and the back-end, which processes data and handles the core functionality. These two parts communicate via APIs. A front-end might send a request for a user's profile data, and the back-end would respond with the necessary details structured in an agreed-upon format. When you use an app like this, your request is communicated over the internet to a data center tens or hundreds of miles away, and the backend responds to it, all in a split second. It's a marvel of communication!

APIs also power many popular services you use daily. Music services like Spotify use APIs to send requests from your app to their servers, fetching your playlists or suggesting new tracks. Social media platforms work similarly—your app communicates with their API to load your feed, post updates, or send messages. 

Beyond individual applications, APIs also enable cross-application integration. For instance, logging into a platform using credentials from Google, Facebook, or GitHub is made possible by authentication APIs. Fitness apps syncing data with health dashboards or e-commerce platforms coordinating with payment processors are other examples of how APIs allow disparate systems to integrate with each other.

## Lessons from History

Each step in the evolution of communication in computing systems reflects a broader goal: making it easier for machines and humans to exchange information. Standardized protocols, structured formats, and accessible APIs have all contributed to this progress, ensuring that systems can collaborate effectively. These are key tools toward arriving at shared understanding between systems and people.