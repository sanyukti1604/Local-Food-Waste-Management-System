SELECT * FROM food_management.food_listings_data;

use food_management;
select Food_ID, Food_Name from food_listings_data;

select sum(provider_id),city from providers
group by city;


select *
from providers;

-- Food Providers & Receivers
-- 1 How many food providers and receivers are there in each city?

SELECT 
    city,
    SUM(provider_count) AS provider_count,
    SUM(receiver_count) AS receiver_count
FROM (
    SELECT 
        city,
        COUNT(provider_id) AS provider_count,
        0 AS receiver_count
    FROM providers
    GROUP BY city

    UNION ALL

    SELECT 
        city,
        0 AS provider_count,
        COUNT(receiver_id) AS receiver_count
    FROM receivers_data
    GROUP BY city
) AS combined
GROUP BY city
ORDER BY city;


-- 2 Which type of food provider (restaurant, grocery store, etc.) contributes the most food?
select Type as providers_Type, count(*) as Total_Donation_Food 
from providers
GROUP BY providers_Type
order by Total_Donation_Food desc;

-- 3 What is the contact information of food providers in a specific city?
select name as food_providers,city,Contact from providers 
order BY city;

-- 4 Which receivers have claimed the most food?

select r.Receiver_ID,r.Name, 
count(c.claim_ID) as  Total_Claims
from receivers_data r
left join claims_data c 
on r.Receiver_ID = c.receiver_ID 
GROUP BY r.receiver_id, r.name
order by total_claims DESC;

-- 2 Food Listings & Availability
-- 2.1 What is the total quantity of food available from all providers?
select f.Provider_ID, sum(f.Quantity) as Total_quantity
 from food_listings_data f
 left join providers p on f.Provider_ID = p.Provider_ID
 GROUP BY f.Provider_ID;


-- 2.2  Which city has the highest number of food listings?
select p.city,Count(f.Food_Type) as food_listing
from food_listings_data f left join providers p on  f.Provider_ID = p.Provider_ID
GROUP BY city
order by food_listing DESC ;#limit 1;

-- 2.3 What are the most commonly available food types?
select f.Food_Type, count(*) as most_available_food 
from food_listings_data f
GROUP BY Food_Type
order by most_available_food DESC;

-- Claims & Distribution
-- 8 How many food claims have been made for each food item?
select f.Food_Name,f.Food_Type,count(c.claim_ID) as Food_Claims 
from food_listings_data f
left join claims_data c on f.Food_ID = c.Food_ID
group by f.Food_Name,f.Food_Type
order by food_claims DESC ;

--  9 Which provider has had the highest number of successful food claims?
select f.provider_ID,count(c.claim_ID) as highest_food_claims 
from food_listings_data f
left join claims_data c on f.Food_ID = c.Food_ID
group by f.provider_ID
order by highest_food_claims DESC limit 1;

-- 10 What percentage of food claims are completed vs. pending vs. canceled?

SELECT 
    Status,
    COUNT(*) AS Total_Claims,
    ROUND(COUNT(*) * 100.0 / t.total_count, 2) AS Percentage
FROM claims_data
CROSS JOIN (
    SELECT COUNT(*) AS total_count
    FROM claims_data
) t
GROUP BY Status, t.total_count
ORDER BY Percentage DESC;

-- 11. What is the average quantity of food claimed per receiver?
SELECT 
    c.Receiver_ID, 
    AVG(f.Quantity) AS Average_Quantity
FROM claims_data c
JOIN food_listings_data f 
    ON c.Food_ID = f.Food_ID
GROUP BY c.Receiver_ID
ORDER BY Average_Quantity DESC;

--  12 Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?
select f.Meal_Type, count(c.Claim_ID) as Most_Claimed_food 
from food_listings_data f 
left join claims_data c  on f.Food_ID = c.Food_ID
GROUP BY f.Meal_Type
ORDER BY Most_Claimed_food DESC;

-- 13.What is the total quantity of food donated by each provider?
select p.Provider_ID,
sum(f.Quantity) As Total_Quantity from providers p 
left join food_listings_data f on p.provider_id = f.provider_id
GROUP BY p.Provider_ID
ORDER BY Total_Quantity;






















