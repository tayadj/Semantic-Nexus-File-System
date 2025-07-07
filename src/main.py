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
	"this is amazing",
	"really terrible experience",
	"I absolutely loved the support I received",
	"I'm completely fed up with this service",
	"best meal I've had in ages",
	"it's a total disaster",
	"thrilled by the efficiency of this tool",
	"extremely disappointed with the outcome",
	"I couldn't be happier with my purchase",
	"I've never been so frustrated"
]

engine = core.Engine()
engine.vectorizer.fit(corpus)

print(engine.vectorizer.tokenizer.token_to_index)
print(engine.sentiment.vectorizer.tokenizer.size)

core.nexus.pipelines.train(engine.sentiment, engine.vectorizer, engine.device)

texts = [
		"this is amazing",
		"really terrible experience",
		"I absolutely loved the support I received",
		"I'm completely fed up with this service",
		"best meal I've had in ages",
		"it's a total disaster",
		"thrilled by the efficiency of this tool",
		"extremely disappointed with the outcome",
		"I couldn't be happier with my purchase",
		"I've never been so frustrated"
]

core.nexus.pipelines.inference(engine.sentiment, texts)