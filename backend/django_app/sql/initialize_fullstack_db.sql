
-- Create the database if it doesn't exist
USE project_db;

INSERT INTO api_store VALUES(1, 'Harris Teeter', 28213, '8600 University City Blvd, Charlotte, NC', 35.296218, -80.738339, '06:00:00', '11:00:00');
INSERT INTO api_store VALUES(2, 'Food Lion', 28262, '9323 N Tryon St, Charlotte, NC', 35.313821, -80.744602, '07:00:00', '11:00:00');
INSERT INTO api_store VALUES(3, 'Walmart Supercenter', 28262, '7735 N Tryon St, Charlotte, NC', 35.295361, -80.758278, '06:00:00', '11:00:00');

INSERT INTO api_item VALUES(1, 'apple');
INSERT INTO api_item VALUES(2, 'banana');
INSERT INTO api_item VALUES(3, 'carrot');
INSERT INTO api_item VALUES(4, 'dog food');
INSERT INTO api_item VALUES(5, 'apricot');
INSERT INTO api_item VALUES(6, 'applesauce');

INSERT INTO api_groceryitem VALUES(1, 'Apple', "Nature's Promise", 1.12, 15, 1, 2);
INSERT INTO api_groceryitem VALUES(2, 'Banana', 'Food Lion', 0.54, 20, 2, 2);
INSERT INTO api_groceryitem VALUES(3, 'Carrot', "Nature's Promise", 0.21, 10, 3, 2);
INSERT INTO api_groceryitem VALUES(4, 'Adult Wet Dog Food', 'Pedigree', 1.99, 12, 4, 2);
INSERT INTO api_groceryitem VALUES(5, 'Apricot Preserves', 'Food Lion', 3.48, 22, 5, 2);
INSERT INTO api_groceryitem VALUES(6, 'Applesauce Cups', "Mott's", 1.12, 9, 6, 2);
INSERT INTO api_groceryitem VALUES(7, 'Apple', "Harris Teeter Farmer's Market", 1.17, 15, 1, 1);
INSERT INTO api_groceryitem VALUES(8, 'Banana', "Harris Teeter Farmer's Market", 0.54, 20, 2, 1);
INSERT INTO api_groceryitem VALUES(9, 'Carrot', "Harris Teeter Farmer's Market", 0.17, 10, 3, 1);
INSERT INTO api_groceryitem VALUES(10, 'Adult Wet Dog Food', 'Pedigree', 1.99, 12, 4, 1);
INSERT INTO api_groceryitem VALUES(11, 'Apricot Preserves', 'Private Selection', 3.99, 22, 5, 1);
INSERT INTO api_groceryitem VALUES(12, 'Applesauce Cups', "Mott's", 3.79, 9, 6, 1);
INSERT INTO api_groceryitem VALUES(13, 'Apple', 'Marketside', 0.73, 49, 1, 3);
INSERT INTO api_groceryitem VALUES(14, 'Banana', 'Marketside', 0.78, 55, 2, 3);
INSERT INTO api_groceryitem VALUES(15, 'Carrot', 'ATV Farms', 0.22, 67, 3, 3);
INSERT INTO api_groceryitem VALUES(16, 'Adult Wet Dog Food', 'Pedigree', 1.82, 36, 4, 3);
INSERT INTO api_groceryitem VALUES(17, 'Apricot Preserves', 'Great Value', 3.66, 27, 5, 3);
INSERT INTO api_groceryitem VALUES(18, 'Applesauce Cups', "Mott's", 2.47, 43, 6, 3);

SELECT COUNT(*) FROM api_store;        
SELECT COUNT(*) FROM api_item;         
SELECT COUNT(*) FROM api_groceryitem;  
SELECT * FROM api_store;
SELECT * FROM api_item;
SELECT * FROM api_groceryitem;
