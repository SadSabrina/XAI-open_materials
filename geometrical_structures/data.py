DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

DAY_CONTEXTS = [
    # Basic
    "It happened on {day} morning.",
    "We met last {day}.",
    "The meeting is on {day}.",
    "She called on {day}.",
    "On {day}, the bell rang.",
    "Every {day} he goes running.",
    "By {day} it was already done.",
    "The train leaves each {day}.",

    # Time of day
   # "{day} morning was unusually quiet.",
    "I'll see you {day} afternoon.",
    "Come by {day} evening.",
    "We stayed until {day} night.",
    "Early {day} morning, it started to rain.",
    "Late {day} evening, everyone left.",

    # Next / last / this
    "See you next {day}.",
    "Last {day} was hectic.",
    "This {day} will be busy.",
    "Until next {day}.",
    "Since last {day}, nothing has changed.",

    # Before / after
    "Before {day}, we need to finish.",
    "After {day}, everything changed.",
    "From {day} onward, the office will be closed.",
    "Starting {day}, new rules apply.",
    "Ending on {day}, the event concludes.",

    # By / until
    "By {day}, the report should be ready.",
    "Finish it before {day}.",
    "The deadline is {day}.",
    "The sale ends on {day}.",
    "The project starts on {day}.",

    # Recurring events
    "Every {day}, she studies French.",
    "Each {day}, we have a meeting.",
    "Classes are held every {day}.",
    "The store is closed every {day}.",
    "Practice takes place each {day}.",

    # Questions
    "Are you free on {day}?",
    "Can we meet {day}?",
    "What are you doing this {day}?",
    "Will you be here next {day}?",
    "Did you call her on {day}?",

    # Statements
    "I arrived on {day}.",
    "He left on {day}.",
    "They returned on {day}.",
    "She starts work on {day}.",
    "The package arrived on {day}.",
    "School begins on {day}.",
    "The conference opens on {day}.",
    "The office reopens on {day}.",

    # Schedule
    "Our appointment is scheduled for {day}.",
    "The interview is on {day}.",
    "The exam takes place on {day}.",
    "The ceremony is this {day}.",
    "Training starts {day}.",

    # Relative references
    "Not until {day} did we know the answer.",
    "As of {day}, the policy changes.",
    "Around {day}, business picks up.",
    "Shortly after {day}, we received the news.",
    "Just before {day}, everything was ready.",

    # Narrative
    "On {day}, everything seemed normal.",
    "It all began on {day}.",
    "Nothing unusual happened until {day}.",
    "The incident occurred late on {day}.",
    "The celebration continued through {day}.",
    "By the end of {day}, everyone was exhausted.",

    # Transport / business
    "Flights resume on {day}.",
    "Deliveries are made every {day}.",
    "The market opens on {day}.",
    "The bank is closed on {day}.",
    "Support is available from {day}.",

    # Informal
    "Let's catch up on {day}.",
    "I'm busy {day}.",
   # "{day} works for me.",
    "How about {day}?",
    "See you on {day}!",
    "Can't wait for {day}.",
]
NUMBERS = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
]

TEMPLATES = [
    "Let's look at some calendar information. The day is {day}, and the number is {number}.",
    "Let's look at some calendar information. The weekday is {day}, and the value is {number}.",
    "Let's look at some calendar information. The given day is {day}, and the given number is {number}.",
    "Let's look at some calendar information. Today is {day}, and the associated number is {number}.",
    "Let's look at some calendar information. The calendar shows {day} together with the number {number}.",
    "Let's look at some calendar information. The entry contains {day} and the number {number}.",
    "Let's look at some calendar information. The recorded weekday is {day}, and the recorded number is {number}.",
    "Let's look at some calendar information. The selected day is {day}, and the selected number is {number}.",
    "Let's look at some calendar information. The example includes {day} and the value {number}.",
    "Let's look at some calendar information. We are given the day {day} and the number {number}.",
]

TEMPLATES_MATH = [
    "Let's do some calendar math. From {day}, {number} days later is",
    "Let's do some calendar math. Starting from {day}, {number} days later is",
    "Let's do some calendar math. If today is {day}, then {number} days later is",
    "Let's do some calendar math. The day {number} days after {day} is",
    "Let's do some calendar math. Moving {number} days forward from {day} gives",
    "Let's do some calendar math. Counting {number} days forward from {day} gives",
    "Let's do some calendar math. Beginning on {day}, the weekday after {number} days is",
    "Let's do some calendar math. Given that today is {day}, the day after {number} days is",
    "Let's do some calendar math. Starting with {day} and moving forward {number} days gives",
    "Let's do some calendar math. The weekday reached {number} days after {day} is",
]