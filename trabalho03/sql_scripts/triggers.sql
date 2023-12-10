CREATE OR REPLACE FUNCTION update_game_mean_rating()
RETURNS TRIGGER AS $$
DECLARE
    total_score NUMERIC;
    rating_count INT;
    mean_rating NUMERIC;
BEGIN
    BEGIN
        -- Calculate total score and count of ratings for the given game
        SELECT COALESCE(SUM(score), 0), COUNT(*) INTO total_score, rating_count
        FROM tb_rating
        WHERE game_id = NEW.game_id;

        -- Calculate mean rating (avoid division by zero)
        IF rating_count > 0 THEN
            mean_rating := total_score / rating_count;
        ELSE
            mean_rating := 0;
        END IF;

        -- Update mean rating in tb_game
        UPDATE tb_game
        SET total_score = mean_rating
        WHERE game_id = NEW.game_id;

    EXCEPTION
        WHEN OTHERS THEN
            -- Log the exception details
            RAISE INFO 'Exception in update_game_mean_rating: %', SQLERRM;
    END;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;