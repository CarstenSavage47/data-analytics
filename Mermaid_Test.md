Flow Chart Left to Right
```mermaid
flowchart LR 
    A --> B
```

You can assign text to a rectangle and also reference that rectangle
with just the letter (etc. B[Hello] Displays Hello but you can refer to it with B).
```mermaid
flowchart 
    A[Start analysis] --> B[Do The Analysis]
    B --> C[Finish the analysis]
```
Different types of diagrams:
```mermaid
flowchart LR 
A[Start] --> B
B(Enter Your email address) --> C{Existing User?};
C -->|No| D(Enter Name)
C -->|Yes| E(Sign in)
D --> F(End)
E --> F
F --> A
```