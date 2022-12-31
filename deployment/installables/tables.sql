DROP TABLE IF EXISTS `user_master`;
CREATE TABLE IF NOT EXISTS `user_master`
(
    `user_id` int(11) NOT NULL AUTO_INCREMENT,
    `pipeline_name` varchar NOT NULL,
    `pipeline_user_id` int(11) NOT NULL AUTO_INCREMENT,
    `user_name` varchar(100) NOT NULL,
    `user_details` json DEFAULT NULL,
    PRIMARY KEY (`user_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `weight_tracker_dtl`;
CREATE TABLE IF NOT EXISTS `weight_tracker_dtl`
(
    `id` int(11) NOT_NULL,
    `pipeline_json` json DEFAULT NULL,
    FOREIGN KEY id REFERENCES user_master(pipeline_user_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
