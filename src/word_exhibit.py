words = [
("laughter","very positive","associated with joy and social bonding"),
("happiness","very positive","represents a positive emotional state"),
("love","very positive","universal symbol of affection"),
("joy","very positive","expresses strong happiness"),
("smile","very positive","linked to positive emotions"),

("death","very negative","associated with loss and fear"),
("suicide","very negative","connected to tragedy and despair"),
("rape","very negative","represents violence and trauma"),
("killing","very negative","associated with violence"),
("murder","very negative","strongly negative violent act"),

("fucking","highly contested","insult but also positive intensifier"),
("pussy","highly contested","cat vs vulgar slang"),
("whiskey","highly contested","leisure vs alcoholism"),
("capitalism","highly contested","political ideology interpreted differently"),
("mortality","highly contested","philosophical vs negative meaning"),

("republicans","culturally loaded","political identity word"),
("religion","cultural loaded","faith vs conflict interpretations"),
("money","cultural loaded","wealth vs greed"),
("freedom","cultural loaded","positive but politically contested"),
("power","cultural loaded","authority vs oppression")
]

print("| Word | Category | Explanation |")
print("|------|-----------|-------------|")

for word,category,explanation in words:
    print(f"| {word} | {category} | {explanation} |")
    