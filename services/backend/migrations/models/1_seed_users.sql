-- upgrade --
DELETE FROM public.userroles;
INSERT INTO public.userroles
(id, "role", "label")
VALUES(1, 'unconfigured_user', 'New user');
INSERT INTO public.userroles
(id, "role", "label")
VALUES(2, 'moderator', 'Moderator');
INSERT INTO public.userroles
(id, "role", "label")
VALUES(3, 'admin', 'Administrator');
INSERT INTO public.users (id,username,full_name,"password",created_at,modified_at,role_id) VALUES
	 (1,'admin@schreppers.com','Admin account','$2b$12$0P5Gbti6JYO8UkHkTAz1geLUlUJD2.lr8hfHWAAWlGX5VfBCwTj9y','2022-09-03 23:17:03.040339+02','2022-09-03 23:17:03.040356+02',3),
   (2,'moderator@schreppers.com','Moderator test account','$2b$12$dxb3vet4WOO2pco9bvbApuIfj.v1CP6i9y4LJAam7KRuyCYq3e9sO','2022-09-03 23:17:03.040339+02','2022-09-03 23:17:03.040356+02',2);
-- downgrade --
DELETE FROM public.userroles;
DELETE FROM public.users;
