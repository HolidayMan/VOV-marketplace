DROP DATABASE vov_database;
CREATE DATABASE vov_database;
USE vov_database;

CREATE TABLE order_status
(
	name                  VARCHAR(40) NOT NULL,
	id                    INTEGER NOT NULL auto_increment,
	 PRIMARY KEY (id)
)
;



CREATE UNIQUE INDEX XAK1order_status ON order_status
(
	name
)
;



CREATE TABLE user_role
(
	id                    BIGINT NOT NULL auto_increment,
	name                  VARCHAR(40) NOT NULL,
	 PRIMARY KEY (id)
)
;



CREATE UNIQUE INDEX XAK1user_role ON user_role
(
	name
)
;



CREATE TABLE user
(
	id                    BIGINT NOT NULL auto_increment,
	name                  TEXT NOT NULL,
	email                 VARCHAR(320) NOT NULL,
	password              VARCHAR(256) NOT NULL,
	role_id               BIGINT NOT NULL,
	 PRIMARY KEY (id), FOREIGN KEY role_to_user (role_id) REFERENCES user_role(id)
)
;



CREATE UNIQUE INDEX XAK1user_email ON user
(
	email,
	role_id
)
;



CREATE TABLE `order`
(
	id                    BIGINT NOT NULL auto_increment,
	status_id             INTEGER NOT NULL,
	customer_id           BIGINT NOT NULL,
	creation_date         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	 PRIMARY KEY (id), FOREIGN KEY order_status_to_order (status_id) REFERENCES order_status(id),
	FOREIGN KEY customer_to_order (customer_id) REFERENCES user(id)
		ON DELETE CASCADE
)
;



CREATE TABLE shop_data
(
	name                  VARCHAR(320) NOT NULL,
	description           TEXT NOT NULL,
	id                    BIGINT NOT NULL auto_increment,
	approved              boolean NOT NULL DEFAULT False,
	 PRIMARY KEY (id)
)
;



CREATE UNIQUE INDEX XAK1shop_data ON shop_data
(
	name
)
;



CREATE TABLE shop
(
	shop_data_id          BIGINT NOT NULL,
	seller_id             BIGINT NOT NULL,
	 PRIMARY KEY (seller_id), FOREIGN KEY shop_data_to_shop (shop_data_id) REFERENCES shop_data(id),
	FOREIGN KEY seller_to_shop (seller_id) REFERENCES user(id)
		ON DELETE CASCADE
)
;



CREATE UNIQUE INDEX XAK1shop ON shop
(
	shop_data_id
)
;



CREATE TABLE product_data
(
	name                  VARCHAR(320) NOT NULL,
	description           TEXT NOT NULL,
	id                    BIGINT NOT NULL auto_increment,
	approved              boolean NOT NULL DEFAULT False,
	image_file_path       TEXT NULL,
	 PRIMARY KEY (id)
)
;



CREATE INDEX XIE1product_data ON product_data
(
	name
)
;



CREATE TABLE product
(
	product_data_id       BIGINT NOT NULL,
	id                    BIGINT NOT NULL auto_increment,
	price                 DECIMAL(10,2) NOT NULL
		CONSTRAINT CHECK (price >= 0),
	seller_id             BIGINT NOT NULL,
	 PRIMARY KEY (id), FOREIGN KEY product_to_product_data (product_data_id) REFERENCES product_data(id),
	FOREIGN KEY R_41 (seller_id) REFERENCES shop(seller_id)
		ON DELETE CASCADE
)
;



CREATE UNIQUE INDEX XAK1product ON product
(
	product_data_id
)
;



CREATE TABLE order_item_status
(
	name                  VARCHAR(40) NOT NULL,
	id                    INTEGER NOT NULL auto_increment,
	 PRIMARY KEY (id)
)
;



CREATE UNIQUE INDEX XAK1order_item_status ON order_item_status
(
	name
)
;



CREATE TABLE order_item
(
	order_id              BIGINT NOT NULL,
	count                 INTEGER NOT NULL DEFAULT 1
		CONSTRAINT CHECK (count >= 1),
	price                 DECIMAL(10,2) NOT NULL
		CONSTRAINT CHECK (price >= 0),
	product_id            BIGINT NOT NULL,
	status_id             INTEGER NOT NULL,
	refuse_reason         TEXT NULL,
	check_date            DATETIME NULL,
	 PRIMARY KEY (order_id,product_id), FOREIGN KEY order_to_order_item (order_id) REFERENCES `order`(id)
		ON DELETE CASCADE,
	FOREIGN KEY product_to_order_item (product_id) REFERENCES product(id),
	FOREIGN KEY order_item_status_to_order_item (status_id) REFERENCES order_item_status(id)
)
;



CREATE TABLE category
(
	id                    BIGINT NOT NULL auto_increment,
	parent_id             BIGINT NULL,
	name                  VARCHAR(320) NOT NULL,
	 PRIMARY KEY (id), FOREIGN KEY sub_category_to_category (parent_id) REFERENCES category(id)
)
;



CREATE UNIQUE INDEX XAK1category ON category
(
	name
)
;



CREATE TABLE product_category
(
	product_id            BIGINT NOT NULL,
	category_id           BIGINT NOT NULL,
	 PRIMARY KEY (product_id,category_id), FOREIGN KEY product_to_ptoduct_category (product_id) REFERENCES product(id)
		ON DELETE CASCADE,
	FOREIGN KEY category_to_product_category (category_id) REFERENCES category(id)
		ON DELETE CASCADE
)
;



CREATE TABLE request_status
(
	name                  VARCHAR(40) NOT NULL,
	id                    INTEGER NOT NULL auto_increment,
	 PRIMARY KEY (id)
)
;



CREATE UNIQUE INDEX XAK1request_status ON request_status
(
	name
)
;



CREATE TABLE add_product_request
(
	seller_id             BIGINT NOT NULL,
	refuse_reason         TEXT NULL,
	moderator_id          BIGINT NULL,
	product_data_id       BIGINT NOT NULL,
	request_status_id     INTEGER NOT NULL,
	creation_date         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	check_date            DATETIME NULL,
	 PRIMARY KEY (product_data_id), FOREIGN KEY product_data_to_add_request (product_data_id) REFERENCES product_data(id)
		ON DELETE CASCADE,
	FOREIGN KEY add_request_to_status (request_status_id) REFERENCES request_status(id),
	FOREIGN KEY moderator_to_add_requests (moderator_id) REFERENCES user(id),
	FOREIGN KEY seller_to_add_requests (seller_id) REFERENCES user(id)
		ON DELETE CASCADE
)
;



CREATE TABLE create_shop_request
(
	refuse_reason         TEXT NULL,
	shop_data_id          BIGINT NOT NULL,
	request_status_id     INTEGER NOT NULL,
	creation_date         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	check_date            DATETIME NULL,
	moderator_id          BIGINT NULL,
	seller_id             BIGINT NOT NULL,
	 PRIMARY KEY (shop_data_id), FOREIGN KEY shop_data_to_create_request (shop_data_id) REFERENCES shop_data(id)
		ON DELETE CASCADE,
	FOREIGN KEY create_request_to_status (request_status_id) REFERENCES request_status(id),
	FOREIGN KEY moderator_to_create_requests (moderator_id) REFERENCES user(id),
	FOREIGN KEY seller_to_create_requests (seller_id) REFERENCES user(id)
		ON DELETE CASCADE
)
;



CREATE TABLE cart_item
(
	count                 INTEGER NOT NULL DEFAULT 1
		CONSTRAINT CHECK (count >= 1),
	product_id            BIGINT NOT NULL,
	customer_id           BIGINT NOT NULL,
	price                 DECIMAL(10,2) NULL
		CONSTRAINT CHECK (price >= 0),
	 PRIMARY KEY (product_id,customer_id), FOREIGN KEY product_to_cart_item (product_id) REFERENCES product(id)
		ON DELETE CASCADE,
	FOREIGN KEY customer_to_cart_items (customer_id) REFERENCES user(id)
		ON DELETE CASCADE
)
;

DELIMITER $$
    CREATE TRIGGER order_status_update_trigger AFTER UPDATE ON order_item FOR EACH ROW
        BEGIN
            DECLARE items_count INT DEFAULT 0;
            DECLARE processed_count INT DEFAULT 0;
            SELECT COUNT(*) INTO items_count FROM order_item WHERE order_id = NEW.order_id;
            SELECT COUNT(*) INTO processed_count FROM order_item
                 JOIN  order_item_status ois ON order_item.status_id = ois.id
                 WHERE order_id = NEW.order_id AND (ois.name = 'accepted' OR ois.name = 'declined');
            IF (items_count = processed_count) THEN
                UPDATE `order` SET `order`.status_id = (SELECT order_status.id
                                                        FROM order_status
                                                        WHERE order_status.name = 'closed')
                WHERE `order`.id = NEW.order_id;
            END IF;
        END $$
DELIMITER ;





