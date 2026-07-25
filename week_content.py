# -*- coding: utf-8 -*-
"""
Single source of truth for the weekly content.

Both push_content.py (Notion) and daily_story.py (IG story PNGs) import WEEK
from here, so the calendar and the images can never drift apart: same hooks,
same named frameworks, same DM keywords.

Theme of this week: "WHERE THE MONEY DIES" -- each day exposes one place a
local service business bleeds leads/cash, and positions the done-for-you
machine (Meta Ads -> landing page -> text automation -> booked calendar ->
your tech shows up) as the plug.

Weekly themes (fixed):
    Monday    -- One Specific Fix   (teach one concrete fix)
    Tuesday   -- Before & After     (real client proof)
    Wednesday -- The Pain           (agitate)
    Thursday  -- Behind The Scenes  (show the work)
    Friday    -- The Framework      (a named, drawn-out system)
    Saturday  -- Objection Crusher  (destroy one objection)
    Sunday    -- rest / repurpose   (no scripts)

Video block field labels used in Notion:
    Content Style / Format, Content Pillar, Hook, Script, CTA, Caption
"""

DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday",
             "Friday", "Saturday", "Sunday"]

# DM keyword per day (Mon-Sat). Sunday has none.
KEYWORDS = {
    "Monday": "FIX",
    "Tuesday": "PROOF",
    "Wednesday": "LEAKS",
    "Thursday": "SYSTEM",
    "Friday": "PLAYBOOK",
    "Saturday": "BOOKED",
}

# Daily to-do checklist (identical Mon-Sat).
CHECKLIST = [
    "Film today's videos (2-3 minimum, aim for all 4)",
    "Write captions + on-screen text for each video",
    "Post to IG + TikTok",
    "Post today's 3 IG stories",
    "Go live 2x on TikTok",
    "Outreach: DM 10 prospects in FB groups + 5 on LinkedIn",
    "Reply to every comment for 1 full hour after posting",
]

# Theme accent colors. 'notion' = Notion callout color option,
# 'rgb' = accent used in the story images.
THEME = {
    "Monday":    {"name": "One Specific Fix",  "notion": "blue_background",   "rgb": (56, 132, 255)},
    "Tuesday":   {"name": "Before & After",    "notion": "green_background",  "rgb": (46, 204, 113)},
    "Wednesday": {"name": "The Pain",          "notion": "red_background",    "rgb": (231, 76, 60)},
    "Thursday":  {"name": "Behind The Scenes", "notion": "orange_background", "rgb": (243, 156, 18)},
    "Friday":    {"name": "The Framework",     "notion": "purple_background", "rgb": (155, 89, 232)},
    "Saturday":  {"name": "Objection Crusher", "notion": "yellow_background", "rgb": (241, 196, 15)},
    "Sunday":    {"name": "Rest / Repurpose",  "notion": "gray_background",   "rgb": (149, 165, 166)},
}


# ---------------------------------------------------------------------------
# THE WEEK
# ---------------------------------------------------------------------------
WEEK = {

    # ===================================================================
    "Monday": {
        "videos": [
            {
                "style": "Talking head",
                "pillar": "Value",
                "hook": "You lose 8 out of 10 leads before lunch.",
                "script": (
                    "[S -- SHOCK, spoken]: You lose 8 out of 10 leads before lunch.\n"
                    "[T -- TEXT HOOK on screen]: \"Your leads rot in 5 minutes.\"\n"
                    "[A -- ACHIEVEMENT]: We book 30+ jobs a month for service businesses "
                    "who used to 'call people back later.'\n"
                    "[R -- ROADMAP]: There's a 300-second window after a lead comes in.\n"
                    "Miss it and the money is already gone.\n"
                    "Stay to the end and I'll hand you The 300-Second Window -- "
                    "the exact way we catch every lead before it goes cold.\n"
                    "[RECIPE]:\n"
                    "1. A lead fills out your form.\n"
                    "2. A text fires in under 60 seconds -- automatically, not 'when you get to it.'\n"
                    "3. It asks one thing: what day works for you?\n"
                    "4. It offers two time slots. Not 'call us.' Two slots.\n"
                    "5. No reply? Three more texts across 48 hours.\n"
                    "[LOOP CLOSE]: That's The 300-Second Window.\n"
                    "The lead never had time to call the next guy.\n"
                    "You didn't get more leads.\n"
                    "You just stopped killing the ones you already paid for."
                ),
                "cta": "Comment or DM \"FIX\" and I'll send you the 5-minute follow-up sequence we install.",
                "caption": ("You're not short on leads. You're short on speed. The 300-Second "
                            "Window is why our clients book the jobs the other guy 'meant to "
                            "call back.' DM FIX."),
            },
            {
                "style": "Overlay text",
                "pillar": "Value",
                "hook": "5 minutes late = a dead lead.",
                "script": (
                    "A lead comes in at 9:02pm.\n"
                    "You see it at 8:15am.\n"
                    "[on screen: -78% chance they answer]\n"
                    "They already booked your competitor.\n"
                    "Here's the timeline that actually wins:\n"
                    "0:00 -- form submitted\n"
                    "0:45 -- auto text sent\n"
                    "2:00 -- they reply 'tomorrow at 10?'\n"
                    "5:00 -- on your calendar.\n"
                    "The lead didn't get better. Your response did."
                ),
                "cta": "DM \"FIX\" for the exact 5-minute timeline.",
                "caption": "Speed is the cheapest upgrade you'll ever buy. DM FIX.",
            },
            {
                "style": "Green screen (SMS screenshot behind me)",
                "pillar": "Proof",
                "hook": "This one text booked a $4,000 job.",
                "script": (
                    "[green screen: a real SMS thread]\n"
                    "Lead came in at 7:41pm.\n"
                    "Our system texted back at 7:41pm. Same minute.\n"
                    "'Hey it's Mike from ___ -- want Thursday 2pm or Friday 9am?'\n"
                    "They picked Friday.\n"
                    "The owner was asleep.\n"
                    "[circle both timestamps]\n"
                    "No human touched this until the tech showed up to the job."
                ),
                "cta": "Want this thread running for you? DM \"FIX\".",
                "caption": "The owner was asleep. The calendar wasn't. DM FIX.",
            },
            {
                "style": "Reaction (reacting to bad advice)",
                "pillar": "Pain",
                "hook": "\"I'll call them back tomorrow\" -- famous last words.",
                "script": (
                    "[react to a clip of an owner saying 'I'll get to it tomorrow']\n"
                    "Stop. That lead is worth $40 right now.\n"
                    "By tomorrow it's worth $4.\n"
                    "They filled out 3 other forms tonight.\n"
                    "Whoever texts first wins the job. Every single time.\n"
                    "You don't have a lead problem.\n"
                    "You have a 12-hour delay problem."
                ),
                "cta": "Kill the delay -- DM \"FIX\".",
                "caption": "Tomorrow is where leads go to die. DM FIX.",
            },
        ],
        "stories": [
            [{"type": "poll",
              "question": "How fast do you text a new lead back?",
              "options": ["Under 5 min", "Honestly... hours"]}],
            [{"type": "text", "box": "dark",
              "text": "A lead goes cold in [r]5 minutes[/].\nYours are sitting overnight."},
             {"type": "text", "box": "white",
              "text": "Our system texts back in [g]under 60 seconds[/]."}],
            [{"type": "text", "box": "white",
              "text": "The 300-Second Window"},
             {"type": "text", "box": "dark",
              "text": "DM me [o]FIX[/] for the 5-minute follow-up sequence we install."}],
        ],
    },

    # ===================================================================
    "Tuesday": {
        "videos": [
            {
                "style": "Talking head",
                "pillar": "Proof",
                "hook": "This plumber did 6 jobs a week. Now he turns work away.",
                "script": (
                    "[S -- SHOCK, spoken]: This plumber did zero ads and 6 jobs a week. "
                    "Now he turns work away.\n"
                    "[T -- TEXT HOOK on screen]: \"From praying for referrals to a full calendar.\"\n"
                    "[A -- ACHIEVEMENT]: 41 booked estimates in 30 days. Same truck, same guy, same town.\n"
                    "[R -- ROADMAP]: Everyone shows you the 'after.'\n"
                    "Nobody shows the switch that flipped.\n"
                    "Stay to the end -- I'll hand you The Proof Stack, the 3 assets that did it.\n"
                    "[RECIPE]:\n"
                    "1. One Meta ad aimed at his 15-mile radius. Not 'awareness.' Booked estimates.\n"
                    "2. A landing page that asked for the job address and the problem -- nothing else.\n"
                    "3. Text automation that confirmed and reminded, so no-shows died.\n"
                    "[LOOP CLOSE]: That's The Proof Stack.\n"
                    "He didn't get more skilled.\n"
                    "He put a machine in front of the skill he already had."
                ),
                "cta": "DM \"PROOF\" and I'll send you the exact 3 assets.",
                "caption": "Same plumber. Same skills. New machine. 41 estimates in 30 days. DM PROOF.",
            },
            {
                "style": "Green screen (results screenshot)",
                "pillar": "Proof",
                "hook": "Here's the calendar that used to be empty.",
                "script": (
                    "[green screen: a booking calendar filling up week by week]\n"
                    "Week 1: 4 estimates.\n"
                    "Week 2: 9.\n"
                    "Week 3: 12.\n"
                    "Week 4: 16.\n"
                    "Same ad budget the entire time.\n"
                    "The ad didn't change. The follow-up did the heavy lifting."
                ),
                "cta": "DM \"PROOF\" for the setup.",
                "caption": "An empty calendar is a follow-up problem. DM PROOF.",
            },
            {
                "style": "Split screen (two owners: wrong vs right)",
                "pillar": "Proof",
                "hook": "Two contractors. One prays. One books.",
                "script": (
                    "LEFT (wrong): 'I just wait for referrals to come in.'\n"
                    "RIGHT (right): 'I've got 12 estimates booked for next week.'\n"
                    "LEFT: 'Some months are dead, some are crazy.'\n"
                    "RIGHT: 'Every week looks the same now.'\n"
                    "LEFT: 'Ads didn't work when I tried them.'\n"
                    "RIGHT: 'Ads plus follow-up. The follow-up is the part you skipped.'"
                ),
                "cta": "Be the right guy -- DM \"PROOF\".",
                "caption": "Referrals are a bonus, not a business. DM PROOF.",
            },
            {
                "style": "Overlay text (before/after over b-roll)",
                "pillar": "Proof",
                "hook": "Before: 6 jobs. After: 41 estimates.",
                "script": (
                    "[over b-roll of the job site]\n"
                    "BEFORE -- [r]6 jobs a week[/], all word of mouth.\n"
                    "BEFORE -- dead every January.\n"
                    "BEFORE -- 'we'll call you' leads that vanished.\n"
                    "AFTER -- [g]41 estimates in 30 days[/].\n"
                    "AFTER -- booked two weeks out.\n"
                    "AFTER -- no-shows cut in half by text reminders.\n"
                    "One machine. Thirty days."
                ),
                "cta": "DM \"PROOF\".",
                "caption": "The 'after' is boring. The switch is everything. DM PROOF.",
            },
        ],
        "stories": [
            [{"type": "poll",
              "question": "Where do most of your jobs come from today?",
              "options": ["Referrals / word of mouth", "A system I control"]}],
            [{"type": "table",
              "header": "PLUMBER -- 30 DAYS",
              "rows": [
                  ["Before", "6 jobs / wk", "before"],
                  ["After", "41 estimates", "after"],
                  ["No-shows", "-52%", "after"],
                  ["New skills needed", "0", "after"],
              ]}],
            [{"type": "text", "box": "white",
              "text": "The [g]Proof Stack[/]: ad + landing page + follow-up."},
             {"type": "text", "box": "dark",
              "text": "DM me [o]PROOF[/] and I'll send the exact 3 assets."}],
        ],
    },

    # ===================================================================
    "Wednesday": {
        "videos": [
            {
                "style": "Talking head",
                "pillar": "Pain",
                "hook": "You're one slow month from laying off your crew.",
                "script": (
                    "[S -- SHOCK, spoken]: You're one slow month from laying off your crew.\n"
                    "[T -- TEXT HOOK on screen]: \"Busy today means nothing.\"\n"
                    "[A -- ACHIEVEMENT]: We've pulled 200+ service businesses out of this exact trap.\n"
                    "[R -- ROADMAP]: There's a loop that eats local businesses alive and they "
                    "never see it.\n"
                    "Stay to the end -- I'll name it and show you the one door out: The Famine Loop.\n"
                    "[RECIPE]:\n"
                    "1. You get busy, so you stop marketing.\n"
                    "2. The jobs finish, and the pipeline is empty.\n"
                    "3. Panic. Discounts. Chasing.\n"
                    "4. You get busy again. You stop marketing again.\n"
                    "5. Repeat until burnout.\n"
                    "[LOOP CLOSE]: That's The Famine Loop.\n"
                    "The door out isn't 'more hustle.'\n"
                    "It's a machine that markets while you're on the tools -- "
                    "so busy weeks and slow weeks stop existing."
                ),
                "cta": "DM \"LEAKS\" -- I'll show you where your pipeline is bleeding.",
                "caption": "Busy is not safe. The Famine Loop is why. DM LEAKS.",
            },
            {
                "style": "Reaction",
                "pillar": "Pain",
                "hook": "\"Business is just slow right now.\" No -- it's leaking.",
                "script": (
                    "[react to an owner saying 'it's a slow season']\n"
                    "It's not the season. It's the leak.\n"
                    "You paid for 40 leads last month.\n"
                    "You called back maybe 12.\n"
                    "You quoted 8.\n"
                    "You followed up with... zero.\n"
                    "That's not a slow month. That's a bucket full of holes."
                ),
                "cta": "Find your holes -- DM \"LEAKS\".",
                "caption": "'Slow season' is usually a follow-up leak. DM LEAKS.",
            },
            {
                "style": "Clone (me playing both characters)",
                "pillar": "Pain",
                "hook": "Watch a busy owner talk to his broke self.",
                "script": (
                    "OWNER (today): 'We're slammed, I don't need ads.'\n"
                    "OWNER (3 weeks later): '...it's completely dead. Where'd everyone go?'\n"
                    "TODAY: 'I'll market when I have time.'\n"
                    "LATER: 'I have nothing but time now.'\n"
                    "TODAY: 'Referrals are enough.'\n"
                    "LATER: 'Referrals dried up in one bad month.'\n"
                    "Same guy. Three weeks apart. That's The Famine Loop."
                ),
                "cta": "DM \"LEAKS\" before the 'later' version shows up.",
                "caption": "Today-you is setting up broke-you. DM LEAKS.",
            },
            {
                "style": "Overlay text",
                "pillar": "Pain",
                "hook": "You paid for 40 leads. You called 12.",
                "script": (
                    "[over b-roll]\n"
                    "40 leads came in. [o]You paid for all 40.[/]\n"
                    "[r]28[/] never got a call back.\n"
                    "[r]6[/] got one call and nothing else.\n"
                    "[g]6[/] got followed up with -- all 6 booked.\n"
                    "You don't need more leads.\n"
                    "You need to stop [r]leaking[/] the ones you already bought."
                ),
                "cta": "DM \"LEAKS\".",
                "caption": "The leads aren't the problem. The leak is. DM LEAKS.",
            },
        ],
        "stories": [
            [{"type": "poll",
              "question": "How many of last month's leads did you follow up 3+ times?",
              "options": ["Almost all", "...barely any"]}],
            [{"type": "text", "box": "dark",
              "text": "You paid for [o]40 leads[/].\nYou followed up with [r]6[/]."},
             {"type": "text", "box": "white",
              "text": "That's not a slow month. That's a [r]leak[/]."}],
            [{"type": "text", "box": "white",
              "text": "Let's plug the holes."},
             {"type": "text", "box": "dark",
              "text": "DM me [o]LEAKS[/] and I'll map where your pipeline bleeds."}],
        ],
    },

    # ===================================================================
    "Thursday": {
        "videos": [
            {
                "style": "Talking head",
                "pillar": "Value",
                "hook": "This is the machine that books your calendar while you sleep.",
                "script": (
                    "[S -- SHOCK, spoken]: This is the machine that books your calendar while you sleep.\n"
                    "[T -- TEXT HOOK on screen]: \"Behind the curtain of a booked calendar.\"\n"
                    "[A -- ACHIEVEMENT]: We've built this exact system for 200+ local businesses.\n"
                    "[R -- ROADMAP]: Most agencies hide how it works so you stay dependent.\n"
                    "I'll show you the whole floor -- The Glass Factory -- "
                    "so you see every gear that turns a click into a booked job.\n"
                    "[RECIPE]:\n"
                    "1. A Meta ad catches someone searching at 9pm.\n"
                    "2. A landing page asks for the problem + address. 30 seconds.\n"
                    "3. Automation texts them back in under a minute.\n"
                    "4. Two time slots offered. They pick one.\n"
                    "5. Reminders fire so they actually show up.\n"
                    "[LOOP CLOSE]: That's The Glass Factory.\n"
                    "Nothing magic -- just every gear doing its job "
                    "while you're on a roof or under a sink."
                ),
                "cta": "DM \"SYSTEM\" and I'll walk you through the build.",
                "caption": "No black box. Here's every gear. DM SYSTEM.",
            },
            {
                "style": "Green screen (build on screen)",
                "pillar": "Value",
                "hook": "Watch me build a $1,500 campaign in 4 minutes.",
                "script": (
                    "[green screen: Meta Ads Manager]\n"
                    "Radius: 15 miles around his shop.\n"
                    "Audience: homeowners, 30+.\n"
                    "One image. One promise. One button: Book an estimate.\n"
                    "[switch to the landing page builder]\n"
                    "Two fields. The problem. The address. Done.\n"
                    "This is what 'run ads' actually means."
                ),
                "cta": "DM \"SYSTEM\" for the build checklist.",
                "caption": "'Run ads' is vague. This is the real build. DM SYSTEM.",
            },
            {
                "style": "Miro board (drawing the flow live)",
                "pillar": "Value",
                "hook": "Let me draw where your leads actually go.",
                "script": (
                    "[Miro: draw a box 'AD']\n"
                    "Ad -> arrow -> box 'LANDING PAGE'.\n"
                    "Landing page -> arrow -> box 'TEXT IN 60 SEC'.\n"
                    "Text -> arrow -> '2 SLOTS OFFERED'.\n"
                    "Slots -> arrow -> 'CALENDAR'.\n"
                    "Calendar -> arrow -> 'YOUR GUY SHOWS UP'.\n"
                    "Every arrow is where most owners drop the lead.\n"
                    "We automate every arrow."
                ),
                "cta": "DM \"SYSTEM\" for the full map.",
                "caption": "Your leads fall through the arrows. We weld them shut. DM SYSTEM.",
            },
            {
                "style": "Overlay text (build steps over b-roll)",
                "pillar": "Value",
                "hook": "6 gears turn a click into a job.",
                "script": (
                    "[over b-roll of the crew working]\n"
                    "1. Ad catches them at 9pm.\n"
                    "2. Landing page in 30 seconds.\n"
                    "3. Auto-text in 60 seconds.\n"
                    "4. Two slots, not 'call us.'\n"
                    "5. Reminders kill no-shows.\n"
                    "6. Your guy shows up and closes.\n"
                    "You only do step 6."
                ),
                "cta": "DM \"SYSTEM\".",
                "caption": "You do the work you love. The machine does the rest. DM SYSTEM.",
            },
        ],
        # Thursday uses a Q&A box instead of the CTA on the last slide.
        "stories": [
            [{"type": "poll",
              "question": "Want to see how the booking machine is built?",
              "options": ["Yes, show me", "I already have one"]}],
            [{"type": "text", "box": "dark",
              "text": "Today we built a full [g]Appointment Engine[/] for a roofer."},
             {"type": "text", "box": "white",
              "text": "Ad -> page -> [o]60-sec text[/] -> calendar."}],
            [{"type": "qa",
              "prompt": "Ask me anything about building a booking machine"}],
        ],
    },

    # ===================================================================
    "Friday": {
        "videos": [
            {
                "style": "Talking head",
                "pillar": "Value",
                "hook": "Five gears stand between a stranger and a booked job.",
                "script": (
                    "[S -- SHOCK, spoken]: Five gears stand between a stranger and a booked job.\n"
                    "[T -- TEXT HOOK on screen]: \"The Appointment Engine, drawn out.\"\n"
                    "[A -- ACHIEVEMENT]: This framework books 30+ jobs a month across 200+ "
                    "local businesses.\n"
                    "[R -- ROADMAP]: Everyone sells 'leads.'\n"
                    "Leads aren't the goal -- booked jobs are.\n"
                    "Stay to the end and I'll hand you all five gears of The Appointment Engine.\n"
                    "[RECIPE]:\n"
                    "1. Traffic -- Meta ads to your service radius.\n"
                    "2. Trap -- a landing page built to capture, not to impress.\n"
                    "3. Text -- automation that replies in 60 seconds.\n"
                    "4. Time -- two calendar slots, booked without a phone call.\n"
                    "5. Tech -- your guy shows up and does what he's great at.\n"
                    "[LOOP CLOSE]: That's The Appointment Engine.\n"
                    "Traffic, Trap, Text, Time, Tech.\n"
                    "Skip one gear and the machine stalls -- "
                    "which is exactly why 'just running ads' never worked for you."
                ),
                "cta": "DM \"PLAYBOOK\" for the full framework.",
                "caption": "Traffic, Trap, Text, Time, Tech. Five gears. DM PLAYBOOK.",
            },
            {
                "style": "Miro board (drawing the framework live)",
                "pillar": "Value",
                "hook": "I'm drawing the whole engine in 60 seconds.",
                "script": (
                    "[Miro: write 'THE APPOINTMENT ENGINE']\n"
                    "Gear 1 -- TRAFFIC (Meta). Draw it.\n"
                    "Gear 2 -- TRAP (landing page). Arrow.\n"
                    "Gear 3 -- TEXT (60-sec automation). Arrow.\n"
                    "Gear 4 -- TIME (calendar). Arrow.\n"
                    "Gear 5 -- TECH (your guy). Arrow.\n"
                    "Miss one gear and the whole thing seizes."
                ),
                "cta": "DM \"PLAYBOOK\".",
                "caption": "Five gears. One stalls, all stall. DM PLAYBOOK.",
            },
            {
                "style": "Clone (two characters, both me)",
                "pillar": "Objection",
                "hook": "\"Ads don't work.\" \"You skipped 4 of the 5 gears.\"",
                "script": (
                    "SKEPTIC: 'I ran ads. Waste of money.'\n"
                    "ME: 'Did you have a landing page?'\n"
                    "SKEPTIC: '...I sent them to my Facebook page.'\n"
                    "ME: 'Auto-text in 60 seconds?'\n"
                    "SKEPTIC: 'I called them when I could.'\n"
                    "ME: 'You had one gear out of five.\n"
                    "That's not ads failing. That's four missing gears.'"
                ),
                "cta": "DM \"PLAYBOOK\" for all five.",
                "caption": "One gear isn't an engine. DM PLAYBOOK.",
            },
            {
                "style": "Green screen (dashboard proof)",
                "pillar": "Proof",
                "hook": "This is the engine running at full speed.",
                "script": (
                    "[green screen: dashboard of bookings]\n"
                    "61 leads this month.\n"
                    "47 replied to the auto-text.\n"
                    "33 booked a slot.\n"
                    "29 showed up.\n"
                    "All five gears turning at once.\n"
                    "That's the difference between 'ads' and an engine."
                ),
                "cta": "DM \"PLAYBOOK\".",
                "caption": "Ads get clicks. Engines get jobs. DM PLAYBOOK.",
            },
        ],
        "stories": [
            [{"type": "poll",
              "question": "How many of the 5 gears do you have?",
              "options": ["4 or 5", "1 or 2"]}],
            [{"type": "text", "box": "white",
              "text": "The [g]Appointment Engine[/]:\nTraffic -> Trap -> Text -> Time -> Tech"},
             {"type": "text", "box": "dark",
              "text": "Skip one gear and it [r]stalls[/]."}],
            [{"type": "text", "box": "dark",
              "text": "DM me [o]PLAYBOOK[/] -- I'll send all 5 gears drawn out."}],
        ],
    },

    # ===================================================================
    "Saturday": {
        "videos": [
            {
                "style": "Talking head",
                "pillar": "Objection",
                "hook": "\"Facebook leads are tire-kickers\" is a lie you tell yourself.",
                "script": (
                    "[S -- SHOCK, spoken]: 'Facebook leads are tire-kickers' is a lie you tell yourself.\n"
                    "[T -- TEXT HOOK on screen]: \"The tire-kicker myth, killed.\"\n"
                    "[A -- ACHIEVEMENT]: Same 'trash' traffic books 30+ real jobs a month once it's filtered.\n"
                    "[R -- ROADMAP]: The tire-kicker isn't the lead's fault -- it's a missing filter.\n"
                    "Stay to the end and I'll give you The Filter Funnel that turns 'trash' "
                    "clicks into booked estimates.\n"
                    "[RECIPE]:\n"
                    "1. Ask for the address on the form. Tire-kickers won't give it.\n"
                    "2. Auto-text a real question. Ghosts self-select out.\n"
                    "3. Offer two time slots. Buyers pick. Browsers don't.\n"
                    "4. Reminders. The ones who show are ready to buy.\n"
                    "[LOOP CLOSE]: That's The Filter Funnel.\n"
                    "You didn't have bad leads.\n"
                    "You had no filter -- so every window-shopper reached you "
                    "and every buyer got ignored."
                ),
                "cta": "DM \"BOOKED\" for the filter.",
                "caption": "There are no tire-kickers. Only missing filters. DM BOOKED.",
            },
            {
                "style": "Reaction (bad advice clip)",
                "pillar": "Objection",
                "hook": "\"Just boost your post!\" -- the worst advice online.",
                "script": (
                    "[react to a clip: 'boost your post to get leads']\n"
                    "Boosting gets you likes from your aunt.\n"
                    "Likes don't show up to estimates.\n"
                    "You need a form, a text-back, and a calendar -- not a boost.\n"
                    "'Ads don't work' usually means 'I boosted a post.'"
                ),
                "cta": "DM \"BOOKED\" for what actually works.",
                "caption": "Boosting is not advertising. DM BOOKED.",
            },
            {
                "style": "Split screen (blames vs filters)",
                "pillar": "Objection",
                "hook": "One owner blames the leads. One filters them.",
                "script": (
                    "LEFT: 'These leads are garbage, nobody's serious.'\n"
                    "RIGHT: 'I asked for the address up front -- the flakes vanished.'\n"
                    "LEFT: 'They never answer the phone.'\n"
                    "RIGHT: 'I text first. The serious ones reply in minutes.'\n"
                    "LEFT: 'Facebook doesn't work for my trade.'\n"
                    "RIGHT: 'Facebook + a filter works for every trade.'"
                ),
                "cta": "DM \"BOOKED\".",
                "caption": "Blame the filter, not the lead. DM BOOKED.",
            },
            {
                "style": "Overlay text",
                "pillar": "Objection",
                "hook": "\"Bad leads\" is a filter problem in disguise.",
                "script": (
                    "[over b-roll]\n"
                    "50 clicks. Sounds like [r]tire-kickers[/]?\n"
                    "Add an address field -> 30 real ones left.\n"
                    "Add a 60-sec text -> 22 reply.\n"
                    "Offer 2 slots -> [g]14 book[/].\n"
                    "Same 50 clicks. A filter, not a miracle."
                ),
                "cta": "DM \"BOOKED\".",
                "caption": "The clicks were fine. The filter was missing. DM BOOKED.",
            },
        ],
        "stories": [
            [{"type": "poll",
              "question": "Ever say 'these leads are all tire-kickers'?",
              "options": ["Every week", "Not anymore"]}],
            [{"type": "text", "box": "dark",
              "text": "[r]'Facebook leads are trash.'[/]"},
             {"type": "text", "box": "white",
              "text": "No -- you had [r]no filter[/].\nSame clicks book [g]14 jobs[/] with one."}],
            [{"type": "text", "box": "dark",
              "text": "DM me [o]BOOKED[/] -- I'll send The Filter Funnel."}],
        ],
    },

    # ===================================================================
    "Sunday": {
        # Rest / repurpose -- no scripts.
        "note": (
            "Rest & repurpose day. No new filming. Do this instead:\n"
            "1. Pick your 2 best-performing videos from the week.\n"
            "2. Cut a 15-second version of each for next week.\n"
            "3. Turn your top hook into a written post.\n"
            "4. Screenshot your best DM conversation -- that's Tuesday's proof.\n"
            "5. Refill your photo folder with this week's job-site pics for the story generator."
        ),
        "stories": [
            [{"type": "text", "box": "white",
              "text": "This week: FIX / PROOF / LEAKS / SYSTEM / PLAYBOOK / BOOKED"},
             {"type": "text", "box": "dark",
              "text": "Rest. Repurpose. Refill the camera roll. [g]Back Monday[/]."}],
        ],
    },
}
