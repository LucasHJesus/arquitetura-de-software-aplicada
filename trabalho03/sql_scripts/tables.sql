CREATE TABLE tb_user (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(40),
    email VARCHAR(60),
    password_key VARCHAR(40)
);  
  
CREATE TABLE tb_game(
    game_id SERIAL PRIMARY KEY,
    title VARCHAR(50),
    developer VARCHAR(50),
    total_score NUMERIC(2,1),
    description VARCHAR(500),
    category VARCHAR(50),
    imageURL VARCHAR(255)
);

CREATE TABLE tb_rating (
    user_id INT,
    game_id INT,
    CONSTRAINT fk_tb_rating_user_id FOREIGN KEY (user_id) REFERENCES tb_user (user_id),
    CONSTRAINT fk_tb_rating_game_id FOREIGN KEY (game_id) REFERENCES tb_game (game_id),
    score NUMERIC(2, 1),
    PRIMARY KEY (user_id, game_id)
);