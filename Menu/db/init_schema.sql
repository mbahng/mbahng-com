CREATE TABLE dishes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    instructions TEXT
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT CHECK (category IN (
        'fruits', 'vegetables', 'protein', 'dairy', 
        'condiment', 'alcohol', 'fats', 'grains'
    )),
    unit TEXT NOT NULL,
    serving_size INTEGER,
    calories REAL,
    protein REAL,
    fiber REAL,
    starch REAL,
    sugar REAL,
    saturated_fat REAL,
    monounsat_fat REAL,
    polyunsat_fat REAL,
    trans_fat REAL,
    cholesterol REAL
);

CREATE TABLE nutrients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    unit TEXT NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT now(),
    name TEXT NOT NULL,
    dish TEXT NOT NULL
);

CREATE TABLE dish_ingredients (
    dish_id INTEGER REFERENCES dishes(id),
    ingredient_id INTEGER REFERENCES ingredients(id),
    quantity REAL NOT NULL,
    PRIMARY KEY (dish_id, ingredient_id)
);

CREATE TABLE ingredient_nutrients (
    ingredient_id INTEGER REFERENCES ingredients(id),
    nutrient_id INTEGER NOT REFERENCES nutrient(id),
    amount_per_100g REAL NOT NULL,
    PRIMARY KEY (ingredient_id, nutrient_id)
);

CREATE TABLE nutrient_benefits (
    id SERIAL PRIMARY KEY,
    nutrient_id INTEGER NOT NULL,
    category TEXT CHECK (category IN (
        'cardiovascular', 'immune_system', 'digestive', 'bone_health', 
        'brain_cognitive', 'eye_vision', 'skin_hair', 'muscle_recovery',
        'energy_metabolism', 'reproductive', 'liver_detox', 'respiratory',
        'nervous_system', 'blood_health', 'anti_inflammatory', 'antioxidant'
    )) NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (nutrient_id) REFERENCES nutrients(id)
);
