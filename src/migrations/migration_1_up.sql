-- CREATE api_keys --
CREATE TABLE IF NOT EXISTS api_keys (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`created_ts` DATETIME,
	`updated_ts` DATETIME,
	`key` TEXT NOT NULL,
	`user_id` INTEGER,
	`enabled` TINYINT(1) DEFAULT True,
	`last_use` DATETIME,
	`expiration` DATETIME);

-- CREATE cluster_cves --
CREATE TABLE IF NOT EXISTS cluster_cves (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`created_ts` DATETIME,
	`updated_ts` DATETIME,
	`observed_ts` DATETIME,
	`scheduled` TINYINT(1) DEFAULT 1,
	`cluster_id` INTEGER,
	`cve_critical_int` INTEGER,
	`cve_critical_nums` TEXT,
	`cve_critical_images` TEXT,
	`cve_high_int` INTEGER,
	`cve_high_nums` TEXT,
	`cve_high_images` TEXT,
	`cve_medium_int` INTEGER,
	`cve_medium_nums` TEXT,
	`cve_medium_images` TEXT,
	`cve_low_int` INTEGER,
	`cve_low_nums` TEXT,
	`cve_low_images` TEXT);

-- CREATE clusters --
CREATE TABLE IF NOT EXISTS clusters (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`created_ts` DATETIME,
	`updated_ts` DATETIME,
	`name` VARCHAR(200),
	`slug_name` VARCHAR(200) UNIQUE,
	`enabled` TINYINT(1) DEFAULT True,
	`version` VARCHAR(200),
	`last_check_in` DATETIME);

-- CREATE entity_metas --
CREATE TABLE IF NOT EXISTS entity_metas (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`created_ts` DATETIME,
	`updated_ts` DATETIME,
	`entity_type` VARCHAR(200),
	`entity_id` INTEGER,
	`name` VARCHAR(200),
	`type` VARCHAR(200),
	`value` VARCHAR(200));

-- CREATE image_build_clusters --
CREATE TABLE IF NOT EXISTS image_build_clusters (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`created_ts` DATETIME,
	`updated_ts` DATETIME,
	`image_build_id` INTEGER NOT NULL,
	`cluster_id` INTEGER NOT NULL,
	`last_seen` DATETIME NOT NULL,
	`first_seen` DATETIME NOT NULL,
	`present` TINYINT(1));

-- CREATE image_builds --
CREATE TABLE IF NOT EXISTS image_builds (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`created_ts` DATETIME,
	`updated_ts` DATETIME,
	`digest` VARCHAR(200) UNIQUE,
	`digest_local` VARCHAR(200),
	`image_id` INTEGER NOT NULL,
	`repository` VARCHAR(250) NOT NULL,
	`tags` TEXT,
	`maintained` TINYINT(1) DEFAULT True,
	`state` VARCHAR(200),
	`state_msg` VARCHAR(200),
	`sync_flag` TINYINT(1),
	`sync_enabled` TINYINT(1) DEFAULT True,
	`sync_last_ts` DATETIME,
	`scan_flag` TINYINT(1),
	`scan_enabled` TINYINT(1) DEFAULT True,
	`scan_last_ts` DATETIME,
	`pending_operation` VARCHAR(200));


-- CREATE image_clusters --
CREATE TABLE IF NOT EXISTS image_clusters (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`created_ts` DATETIME,
	`updated_ts` DATETIME,
	`image_id` INTEGER NOT NULL,
	`cluster_id` INTEGER NOT NULL,
	`last_seen` DATETIME NOT NULL,
	`first_seen` DATETIME NOT NULL,
	`present` TINYINT(1));

-- CREATE images --
CREATE TABLE IF NOT EXISTS images (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`created_ts` DATETIME,
	`updated_ts` DATETIME,
	`name` VARCHAR(200) UNIQUE,
	`repositories` TEXT NOT NULL,
	`maintained` TINYINT(1) DEFAULT True,
	`state` VARCHAR(200),
	`state_msg` VARCHAR(200));

-- CREATE operations --
CREATE TABLE IF NOT EXISTS operations (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`created_ts` DATETIME,
	`updated_ts` DATETIME,
	`type` VARCHAR(200),
	`sub_type` VARCHAR(200),
	`entity_type` VARCHAR(200),
	`entity_id` INTEGER,
	`build_id` VARCHAR(200),
	`start_ts` DATETIME,
	`end_ts` DATETIME,
	`result` TINYINT(1),
	`message` TEXT);

-- CREATE options --
CREATE TABLE IF NOT EXISTS options (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`created_ts` DATETIME,
	`updated_ts` DATETIME,
	`name` VARCHAR(200),
	`type` VARCHAR(200),
	`value` VARCHAR(200));

-- CREATE perms --
CREATE TABLE IF NOT EXISTS perms(
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`created_ts` DATETIME,
	`updated_ts` DATETIME,
	`name` VARCHAR(200),
	`slug_name` VARCHAR(200));

-- CREATE requests --
CREATE TABLE IF NOT EXISTS requests (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`created_ts` DATETIME,
	`updated_ts` DATETIME,
	`user_id` INTEGER,
	`request_id` VARCHAR(200),
	`request_ip` VARCHAR(200),
	`request_agent` VARCHAR(200),
	`request_uri` VARCHAR(200),
	`request_method` VARCHAR(200),
	`request_payload` TEXT,
	`response_code` INTEGER,
	`access_perm_slug` VARCHAR(200),
	`authenticated` TINYINT(1));


-- CREATE role_perms --
CREATE TABLE IF NOT EXISTS role_perms (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`created_ts` DATETIME,
	`updated_ts` DATETIME,
	`role_id` INTEGER,
	`perm_id` INTEGER,
	`enabled` TINYINT(1) DEFAULT True);

-- CREATE roles --
CREATE TABLE IF NOT EXISTS roles (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`created_ts` DATETIME,
	`updated_ts` DATETIME,
	`name` VARCHAR(200),
	`slug_name` VARCHAR(200));




-- CREATE scanners --
CREATE TABLE IF NOT EXISTS scanners (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`created_ts` DATETIME,
	`updated_ts` DATETIME,
	`name` VARCHAR(200),
	`build_name` VARCHAR(200),
	`parser_name` VARCHAR(200),
	`enabled` TINYINT(1) DEFAULT 1);

-- CREATE scans --
CREATE TABLE IF NOT EXISTS scans (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`created_ts` DATETIME,
	`updated_ts` DATETIME,
	`image_id` INTEGER,
	`image_build_id` INTEGER,
	`scanner_id` INTEGER,
	`operation_id` INTEGER,
	`codebuild_id` VARCHAR(200),
	`ended_ts` DATETIME,
	`scan_job_success` TINYINT(1),
	`scan_score` TINYINT(1),
	`cve_critical_int` INTEGER DEFAULT 0,
	`cve_critical_nums` TEXT,
	`cve_high_int` INTEGER DEFAULT 0,
	`cve_high_nums` TEXT,
	`cve_medium_int` INTEGER DEFAULT 0,
	`cve_medium_nums` TEXT,
	`cve_low_int` INTEGER DEFAULT 0,
	`cve_low_nums` TEXT,
	`cve_unknown_int` INTEGER DEFAULT 0,
	`cve_unknown_nums` TEXT);

-- CREATE users --
CREATE TABLE IF NOT EXISTS users (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`created_ts` DATETIME,
	`updated_ts` DATETIME,
	`name` VARCHAR(200),
	`last_login` DATETIME,
	`role_id` INTEGER,
	`client_id` VARCHAR(200),
	`client_secret` VARCHAR(200));
