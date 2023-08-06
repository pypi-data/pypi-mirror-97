--------------------------------
-- Weight
--------------------------------

SELECT
  profiles.name,
  date,
  ROUND(bio_log_entry.value * 2.204, 1) AS weight
FROM
  biometric_log
  INNER JOIN profiles ON profile_id = profiles.id
  INNER JOIN bio_log_entry ON biometric_id = 2
    AND log_id = biometric_log.id
WHERE
  profiles.name = 'Mark';

--------------------------------
-- Pulse and blood pressure
--------------------------------

SELECT DISTINCT
  date,
  profiles.name,
  tags,
  notes,
  CAST(sys.value AS int) || '/' || CAST(dia.value AS int) AS pressure,
  CAST(pulse.value AS int) AS pulse
FROM
  biometric_log
  INNER JOIN profiles ON profile_id = profiles.id
  INNER JOIN bio_log_entry pulse ON pulse.biometric_id = 22
    AND pulse.log_id = biometric_log.id
  INNER JOIN bio_log_entry sys ON sys.biometric_id = 23
    AND sys.log_id = biometric_log.id
  INNER JOIN bio_log_entry dia ON dia.biometric_id = 24
    AND dia.log_id = biometric_log.id
WHERE
  profiles.name = 'Mark';

--------------------------------
-- Height, wrist, ankle
--------------------------------

SELECT
  date,
  profiles.name,
  height.value AS height,
  wrist.value AS wrist,
  ankle.value AS ankle
FROM
  biometric_log
  INNER JOIN profiles ON profile_id = profiles.id
  LEFT JOIN bio_log_entry height ON height.biometric_id = 1
    AND height.log_id = biometric_log.id
  LEFT JOIN bio_log_entry wrist ON wrist.biometric_id = 3
    AND wrist.log_id = biometric_log.id
  LEFT JOIN bio_log_entry ankle ON ankle.biometric_id = 4
    AND ankle.log_id = biometric_log.id
WHERE
  height.value
  OR wrist.value
  OR ankle.value;

--------------------------------
-- Measurements (cm)
--------------------------------

SELECT
  date,
  profiles.name,
  chest.value / 2.54 AS chest,
  arm.value / 2.54 AS arm,
  thigh.value / 2.54 AS thigh,
  calf.value / 2.54 AS calf,
  shoulders.value / 2.54 AS shoulders,
  waist.value / 2.54 AS waist,
  hips.value / 2.54 AS hips,
  neck.value / 2.54 AS neck,
  forearm.value / 2.54 AS forearm
FROM
  biometric_log
  INNER JOIN profiles ON profile_id = profiles.id
  LEFT JOIN bio_log_entry chest ON chest.biometric_id = 5
    AND chest.log_id = biometric_log.id
  LEFT JOIN bio_log_entry arm ON arm.biometric_id = 6
    AND arm.log_id = biometric_log.id
  LEFT JOIN bio_log_entry thigh ON thigh.biometric_id = 7
    AND thigh.log_id = biometric_log.id
  LEFT JOIN bio_log_entry calf ON calf.biometric_id = 8
    AND calf.log_id = biometric_log.id
  LEFT JOIN bio_log_entry shoulders ON shoulders.biometric_id = 9
    AND shoulders.log_id = biometric_log.id
  LEFT JOIN bio_log_entry waist ON waist.biometric_id = 10
    AND waist.log_id = biometric_log.id
  LEFT JOIN bio_log_entry hips ON hips.biometric_id = 11
    AND hips.log_id = biometric_log.id
  LEFT JOIN bio_log_entry neck ON neck.biometric_id = 12
    AND neck.log_id = biometric_log.id
  LEFT JOIN bio_log_entry forearm ON forearm.biometric_id = 13
    AND forearm.log_id = biometric_log.id
WHERE
  chest.value
  OR arm.value
  OR thigh.value
  OR calf.value
  OR shoulders.value
  OR waist.value
  OR hips.value
  OR neck.value
  OR forearm.value;

--------------------------------
-- Skinfolds (mm)
--------------------------------

SELECT
  date,
  profiles.name,
  CAST(pectoral.value AS int) AS pec,
  CAST(abdominal.value AS int) AS ab,
  CAST(quadricep.value AS int) AS quad,
  CAST(midaxillar.value AS int) AS midax,
  CAST(subscapular.value AS int) AS sub,
  CAST(tricep.value AS int) AS tricep,
  CAST(suprailiac.value AS int) AS supra
FROM
  biometric_log
  INNER JOIN profiles ON profile_id = profiles.id
  LEFT JOIN bio_log_entry pectoral ON pectoral.biometric_id = 14
    AND pectoral.log_id = biometric_log.id
  LEFT JOIN bio_log_entry abdominal ON abdominal.biometric_id = 15
    AND abdominal.log_id = biometric_log.id
  LEFT JOIN bio_log_entry quadricep ON quadricep.biometric_id = 16
    AND quadricep.log_id = biometric_log.id
  LEFT JOIN bio_log_entry midaxillar ON midaxillar.biometric_id = 17
    AND midaxillar.log_id = biometric_log.id
  LEFT JOIN bio_log_entry subscapular ON subscapular.biometric_id = 18
    AND subscapular.log_id = biometric_log.id
  LEFT JOIN bio_log_entry tricep ON tricep.biometric_id = 19
    AND tricep.log_id = biometric_log.id
  LEFT JOIN bio_log_entry suprailiac ON suprailiac.biometric_id = 20
    AND suprailiac.log_id = biometric_log.id
WHERE
  pectoral.value
  OR abdominal.value
  OR quadricep.value
  OR midaxillar.value
  OR subscapular.value
  OR tricep.value
  OR suprailiac.value;

--------------------------------
-- Recipes overview
--------------------------------

SELECT
  id,
  name,
  COUNT(recipe_id) AS n_foods,
  SUM(grams) AS grams,
  guid,
  created
FROM
  recipes
  LEFT JOIN recipe_dat ON recipe_id = id
GROUP BY
  id;

--------------------------------
-- Last sync
--------------------------------

SELECT
  max((
    SELECT
      last_sync FROM profiles), (
    SELECT
      last_sync FROM biometric_log), (
    SELECT
      last_sync FROM recipes), (
    SELECT
      last_sync FROM food_log), (
    SELECT
      last_sync FROM recipe_log), (
    SELECT
      last_sync FROM rda)) AS last_sync;

