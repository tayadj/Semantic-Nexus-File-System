import torch

import core



corpus = [
	"While eating at a restaurant is an enjoyable and convenient occasional treat, most individuals and families prepare their meals at home.",
	"To make breakfast, lunch, and dinner daily, these persons must have the required foods and ingredients on hand and ready to go; foods and ingredients are typically purchased from a grocery store, or an establishment that distributes foods, drinks, household products, and other items that're used by the typical consumer.",
	"Home cooks often rely on fresh fruits, vegetables, and lean proteins sourced from local farms or specialty markets.",
	"Pantry staples like rice, pasta, beans, lentils, canned tomatoes, and dried herbs ensure you can whip up a quick meal any day of the week.",
	"Spices such as cumin, coriander, turmeric, paprika, and cinnamon add depth and complexity to both savory dishes and baked goods.",
	"Essential utensils include a sharp chef’s knife, a sturdy cutting board, mixing bowls, measuring cups, a spatula, and a whisk.",
	"Cooking methods range from grilling and roasting to sautéing, steaming, and slow-cooking in a crockpot or Dutch oven.",
	"Meal planning helps busy families organize ingredients, prep steps, and portion sizes to reduce food waste and save time.",
	"Some consumers follow dietary preferences—vegan, gluten-free, paleo, or low-carb—which dictate the selection of ingredients and recipes.",
	"Dairy products like milk, cheese, yogurt, and butter feature prominently in breakfasts, sauces, and baking.",
	"Baking bread or pastries requires flour, yeast, water, salt, precise temperature control, and adequate proofing time.",
	"Kitchen appliances—ovens, stovetops, slow cookers, microwaves, blenders, and stand mixers—increase versatility and efficiency.",
	"Leftover meats, vegetables, and grains can be repurposed into hearty soups, stews, stir-fries, or casseroles.",
	"Seasonal produce—from spring asparagus and summer berries to autumn squash and winter root vegetables—guides menu creativity.",
	"Organic, fair-trade, and sustainably sourced products appeal to environmentally and socially conscious shoppers.",
	"Bulk bins for grains, nuts, and legumes let customers buy only what they need, cutting down on packaging waste.",
	"Household essentials—cleaning supplies, paper goods, and storage containers—are also stocked alongside food items.",
	"Specialty sections for international ingredients offer everything from soy sauce and rice vinegar to curry pastes and exotic spices.",
	"very bad",
	"amazing",
	"terrible service",
	"I love this product",
	"worst experience ever",
	"best purchase I've made",
	"I hate it",
	"highly recommend",
	"not worth the money",
	"absolutely fantastic",
	"very disappointing",
	"exceeded my expectations",
	"I will never buy this again",
	"superb quality",
	"it's awful",
	"I'm so happy with this",
	"complete waste",
	"incredible value",
	"not as described",
	"truly enjoyable",
]

engine = core.Engine()
engine.vectorizer.fit(corpus)

print(engine.vectorizer.tokenizer.token_to_index)
print(engine.sentiment.vectorizer.tokenizer.size)



sentiment_texts = [
	"very bad",
	"amazing",
	"terrible service",
	"I love this product",
	"worst experience ever",
	"best purchase I've made",
	"I hate it",
	"highly recommend",
	"not worth the money",
	"absolutely fantastic",
	"very disappointing",
	"exceeded my expectations",
	"I will never buy this again",
	"superb quality",
	"it's awful",
	"I'm so happy with this",
	"complete waste",
	"incredible value",
	"not as described",
	"truly enjoyable",
]

sentiment_labels = [
	0,  
	1,  
	0,  
	1,  
	0,  
	1, 
	0,  
	1,  
	0,  
	1,  
	0,  
	1,  
	0,  
	1,  
	0, 
	1, 
	0, 
	1,  
	0, 
	1, 
]

device = torch.device("cpu")
engine.sentiment.to(device)

dataset = core.nexus.services.sentiment.Dataset(sentiment_texts, sentiment_labels, engine.vectorizer.tokenizer)
loader = torch.utils.data.DataLoader(dataset, batch_size = 2, shuffle = True, collate_fn = core.nexus.services.sentiment.collate)

optimizer = torch.optim.Adam(engine.sentiment.parameters(), lr = 1e-3)
criterion = torch.nn.CrossEntropyLoss()

engine.sentiment.train()
epochs = 10

for epoch in range(1, epochs + 1):

	total_loss = 0.0

	for indices, labels in loader:

		batch = [
			" ".join(engine.vectorizer.tokenizer.index_to_token[index.item()]
			for index in sequence if index.item() != engine.vectorizer.tokenizer.index_padding)
			for sequence in indices
		]

		logits = engine.sentiment(batch)
		loss = criterion(logits, labels.to(device))

		optimizer.zero_grad()
		loss.backward()
		optimizer.step()
		total_loss += loss.item()

	average_loss = total_loss / len(loader)

	print(f"Epoch {epoch:02d}/{epochs}, Loss: {average_loss:.4f}")



engine.sentiment.eval()

texts = [
	"this is amazing",
	"really terrible experience"
]

with torch.no_grad():

	logits = engine.sentiment(texts)
	probabilities = torch.nn.functional.softmax(logits, dim = 1)
	predictions = torch.argmax(probabilities, dim = 1)

for text, probability, prediction in zip(texts, probabilities, predictions):

	print(f"\"{text}\" -> {prediction} ({probability})")