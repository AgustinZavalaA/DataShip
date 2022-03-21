-- populate dataship database 

-- populate users table
INSERT INTO users (name, username, email, password, created_at) 
    VALUES 
        ('Admin', 'admin',NULL, '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', DATE('now')),
        ('Agustin Zavala Arias', 'agus', '1930120@upv.edu.mx', '37d4cc4e380b9d4dc8c42ac018dec3c2f58e65b118ef75dadc2d1125857491f6', DATE('now')),
        ('Daniel Sanchez Sanchez', 'daniel', NULL, 'bd3dae5fb91f88a4f0978222dfd58f59a124257cb081486387cbae9df11fb879', DATE('now'));

-- populate feedback_type table
INSERT INTO feedback_type (id, name, created_at) 
    VALUES 
        (1, 'Bug', DATE('now')),
        (2, 'Feature', DATE('now')),
        (3, 'Vulnerability', DATE('now'));

-- populate modules table
-- TODO: add description to modules
INSERT INTO modules(name, description, created_at)
    VALUES
        ('Mean', '', DATE('now')),
        ('Median', '', DATE('now')),
        ('Mode', '', DATE('now')),
        ('Standard Deviation', '', DATE('now')),
        ('Variance', '', DATE('now')),
        ('Linear Regression', '', DATE('now')),
        ('Clusterization', '', DATE('now')),
        ('Graphing', '', DATE('now'));

-- populate feedback_post table
INSERT INTO feedback_post(type_id, title, post, created_at, user_id, done)
    VALUES
        (1, 'Bug in Mean', 'I found a bug in the mean function', DATE('now'), NULL, 0),
        (2, 'Feature in Mean', 'I would like to add a feature to the mean function', DATE('now'), NULL, 0),
        (3, 'Vulnerability in Mean', 'I found a vulnerability in the mean function', DATE('now'), NULL, 0),
        (1, 'Bug in Median', 'I found a bug in the median function', DATE('now'), NULL, 0),
        (2, 'Feature in Median', 'I would like to add a feature to the median function', DATE('now'), NULL, 0),
        (3, 'Vulnerability in Median', 'I found a vulnerability in the median function', DATE('now'), NULL, 0),
        (1, 'Bug in Mode', 'I found a bug in the mode function', DATE('now'), NULL, 0),
        (2, 'Feature in Mode', 'I would like to add a feature to the mode function', DATE('now'), NULL, 0),
        (3, 'Vulnerability in Mode', 'I found a vulnerability in the mode function', DATE('now'), NULL, 0),
        (1, 'Bug in Standard Deviation', 'I found a bug in the standard deviation function', DATE('now'), NULL, 0),
        (2, 'Feature in Standard Deviation', 'I would like to add a feature to the standard deviation function', DATE('now'), NULL, 0),
        (3, 'Vulnerability in Standard Deviation', 'I found a vulnerability in the standard deviation function', DATE('now'), NULL, 0),
        (1, 'Bug in Variance', 'I found a bug in the variance function', DATE('now'), NULL, 0),
        (2, 'Feature in Variance', 'I would like to add a feature to the variance function', DATE('now'), NULL, 0),
        (3, 'Vulnerability in Variance', 'I found a vulnerability in the variance function', DATE('now'), NULL, 0),
        (1, 'Bug in Linear Regression', 'I found a bug in the linear regression function', DATE('now'), NULL, 0),
        (2, 'Feature in Linear Regression', 'I would like to add a feature to the linear regression function', DATE('now'), NULL, 0);