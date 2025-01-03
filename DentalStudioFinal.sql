PGDMP                      |            DentalStudioFinal    16.2    16.2 6    ,           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            -           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            .           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            /           1262    25713    DentalStudioFinal    DATABASE     �   CREATE DATABASE "DentalStudioFinal" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
 #   DROP DATABASE "DentalStudioFinal";
                postgres    false            �            1259    25749    appointment    TABLE     �  CREATE TABLE public.appointment (
    appointment_id integer NOT NULL,
    medical_result_id integer,
    patient_id integer,
    payment_id integer,
    appointment_date date NOT NULL,
    appointment_time time without time zone NOT NULL,
    appointment_reason character varying(128) NOT NULL,
    appointment_status character varying(128) NOT NULL,
    appointment_delete boolean DEFAULT false
);
    DROP TABLE public.appointment;
       public         heap    postgres    false            �            1259    25748    appointment_appointment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.appointment_appointment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.appointment_appointment_id_seq;
       public          postgres    false    224            0           0    0    appointment_appointment_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.appointment_appointment_id_seq OWNED BY public.appointment.appointment_id;
          public          postgres    false    223            �            1259    25772    appointment_treatment    TABLE     �   CREATE TABLE public.appointment_treatment (
    appointment_treatment_id integer NOT NULL,
    appointment_id integer,
    treatment_id integer,
    quantity integer NOT NULL,
    appointment_treatment_delete boolean DEFAULT false
);
 )   DROP TABLE public.appointment_treatment;
       public         heap    postgres    false            �            1259    25771 2   appointment_treatment_appointment_treatment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.appointment_treatment_appointment_treatment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 I   DROP SEQUENCE public.appointment_treatment_appointment_treatment_id_seq;
       public          postgres    false    226            1           0    0 2   appointment_treatment_appointment_treatment_id_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public.appointment_treatment_appointment_treatment_id_seq OWNED BY public.appointment_treatment.appointment_treatment_id;
          public          postgres    false    225            �            1259    25725    medical_result    TABLE     (  CREATE TABLE public.medical_result (
    medical_result_id integer NOT NULL,
    medical_condition character varying(128) NOT NULL,
    medical_diagnosis character varying(128) NOT NULL,
    medical_prescription character varying(128) NOT NULL,
    medical_result_delete boolean DEFAULT false
);
 "   DROP TABLE public.medical_result;
       public         heap    postgres    false            �            1259    25724 $   medical_result_medical_result_id_seq    SEQUENCE     �   CREATE SEQUENCE public.medical_result_medical_result_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE public.medical_result_medical_result_id_seq;
       public          postgres    false    218            2           0    0 $   medical_result_medical_result_id_seq    SEQUENCE OWNED BY     m   ALTER SEQUENCE public.medical_result_medical_result_id_seq OWNED BY public.medical_result.medical_result_id;
          public          postgres    false    217            �            1259    25715    patient    TABLE     �  CREATE TABLE public.patient (
    patient_id integer NOT NULL,
    patient_last_m character varying(128) NOT NULL,
    patient_first_m character varying(128) NOT NULL,
    patient_middle_m character varying(128),
    patient_bd date NOT NULL,
    age integer NOT NULL,
    sex character varying(128) NOT NULL,
    patient_cn bigint NOT NULL,
    patient_email character varying(128) NOT NULL,
    street character varying(128) NOT NULL,
    barangay character varying(128) NOT NULL,
    city character varying(128) NOT NULL,
    postal_code integer NOT NULL,
    account_creation_date date NOT NULL,
    patient_delete boolean DEFAULT false
);
    DROP TABLE public.patient;
       public         heap    postgres    false            �            1259    25714    patient_patient_id_seq    SEQUENCE     �   CREATE SEQUENCE public.patient_patient_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.patient_patient_id_seq;
       public          postgres    false    216            3           0    0    patient_patient_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.patient_patient_id_seq OWNED BY public.patient.patient_id;
          public          postgres    false    215            �            1259    25741    payment    TABLE     1  CREATE TABLE public.payment (
    payment_id integer NOT NULL,
    payment_date date NOT NULL,
    payment_amount bigint NOT NULL,
    payment_status character varying(128) NOT NULL,
    paid_amount bigint NOT NULL,
    remarks character varying(128) NOT NULL,
    payment_delete boolean DEFAULT false
);
    DROP TABLE public.payment;
       public         heap    postgres    false            �            1259    25740    payment_payment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.payment_payment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.payment_payment_id_seq;
       public          postgres    false    222            4           0    0    payment_payment_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.payment_payment_id_seq OWNED BY public.payment.payment_id;
          public          postgres    false    221            �            1259    25733 	   treatment    TABLE       CREATE TABLE public.treatment (
    treatment_id integer NOT NULL,
    treatment_m character varying(128) NOT NULL,
    treatment_description character varying(128) NOT NULL,
    treatment_price integer NOT NULL,
    treatment_delete boolean DEFAULT false
);
    DROP TABLE public.treatment;
       public         heap    postgres    false            �            1259    25732    treatment_treatment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.treatment_treatment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.treatment_treatment_id_seq;
       public          postgres    false    220            5           0    0    treatment_treatment_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.treatment_treatment_id_seq OWNED BY public.treatment.treatment_id;
          public          postgres    false    219            �            1259    25789    users    TABLE     �   CREATE TABLE public.users (
    user_name character varying(32),
    user_password character varying(64) NOT NULL,
    user_modified_on timestamp without time zone DEFAULT now(),
    user_delete_ind boolean DEFAULT false
);
    DROP TABLE public.users;
       public         heap    postgres    false            u           2604    25752    appointment appointment_id    DEFAULT     �   ALTER TABLE ONLY public.appointment ALTER COLUMN appointment_id SET DEFAULT nextval('public.appointment_appointment_id_seq'::regclass);
 I   ALTER TABLE public.appointment ALTER COLUMN appointment_id DROP DEFAULT;
       public          postgres    false    224    223    224            w           2604    25775 .   appointment_treatment appointment_treatment_id    DEFAULT     �   ALTER TABLE ONLY public.appointment_treatment ALTER COLUMN appointment_treatment_id SET DEFAULT nextval('public.appointment_treatment_appointment_treatment_id_seq'::regclass);
 ]   ALTER TABLE public.appointment_treatment ALTER COLUMN appointment_treatment_id DROP DEFAULT;
       public          postgres    false    225    226    226            o           2604    25728     medical_result medical_result_id    DEFAULT     �   ALTER TABLE ONLY public.medical_result ALTER COLUMN medical_result_id SET DEFAULT nextval('public.medical_result_medical_result_id_seq'::regclass);
 O   ALTER TABLE public.medical_result ALTER COLUMN medical_result_id DROP DEFAULT;
       public          postgres    false    217    218    218            m           2604    25718    patient patient_id    DEFAULT     x   ALTER TABLE ONLY public.patient ALTER COLUMN patient_id SET DEFAULT nextval('public.patient_patient_id_seq'::regclass);
 A   ALTER TABLE public.patient ALTER COLUMN patient_id DROP DEFAULT;
       public          postgres    false    215    216    216            s           2604    25744    payment payment_id    DEFAULT     x   ALTER TABLE ONLY public.payment ALTER COLUMN payment_id SET DEFAULT nextval('public.payment_payment_id_seq'::regclass);
 A   ALTER TABLE public.payment ALTER COLUMN payment_id DROP DEFAULT;
       public          postgres    false    222    221    222            q           2604    25736    treatment treatment_id    DEFAULT     �   ALTER TABLE ONLY public.treatment ALTER COLUMN treatment_id SET DEFAULT nextval('public.treatment_treatment_id_seq'::regclass);
 E   ALTER TABLE public.treatment ALTER COLUMN treatment_id DROP DEFAULT;
       public          postgres    false    219    220    220            &          0    25749    appointment 
   TABLE DATA           �   COPY public.appointment (appointment_id, medical_result_id, patient_id, payment_id, appointment_date, appointment_time, appointment_reason, appointment_status, appointment_delete) FROM stdin;
    public          postgres    false    224   �H       (          0    25772    appointment_treatment 
   TABLE DATA           �   COPY public.appointment_treatment (appointment_treatment_id, appointment_id, treatment_id, quantity, appointment_treatment_delete) FROM stdin;
    public          postgres    false    226    I                  0    25725    medical_result 
   TABLE DATA           �   COPY public.medical_result (medical_result_id, medical_condition, medical_diagnosis, medical_prescription, medical_result_delete) FROM stdin;
    public          postgres    false    218   I                 0    25715    patient 
   TABLE DATA           �   COPY public.patient (patient_id, patient_last_m, patient_first_m, patient_middle_m, patient_bd, age, sex, patient_cn, patient_email, street, barangay, city, postal_code, account_creation_date, patient_delete) FROM stdin;
    public          postgres    false    216   :I       $          0    25741    payment 
   TABLE DATA           �   COPY public.payment (payment_id, payment_date, payment_amount, payment_status, paid_amount, remarks, payment_delete) FROM stdin;
    public          postgres    false    222   WI       "          0    25733 	   treatment 
   TABLE DATA           x   COPY public.treatment (treatment_id, treatment_m, treatment_description, treatment_price, treatment_delete) FROM stdin;
    public          postgres    false    220   tI       )          0    25789    users 
   TABLE DATA           \   COPY public.users (user_name, user_password, user_modified_on, user_delete_ind) FROM stdin;
    public          postgres    false    227   �I       6           0    0    appointment_appointment_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.appointment_appointment_id_seq', 1, false);
          public          postgres    false    223            7           0    0 2   appointment_treatment_appointment_treatment_id_seq    SEQUENCE SET     a   SELECT pg_catalog.setval('public.appointment_treatment_appointment_treatment_id_seq', 1, false);
          public          postgres    false    225            8           0    0 $   medical_result_medical_result_id_seq    SEQUENCE SET     S   SELECT pg_catalog.setval('public.medical_result_medical_result_id_seq', 1, false);
          public          postgres    false    217            9           0    0    patient_patient_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.patient_patient_id_seq', 1, false);
          public          postgres    false    215            :           0    0    payment_payment_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.payment_payment_id_seq', 1, false);
          public          postgres    false    221            ;           0    0    treatment_treatment_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.treatment_treatment_id_seq', 1, false);
          public          postgres    false    219            �           2606    25755    appointment appointment_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_pkey PRIMARY KEY (appointment_id);
 F   ALTER TABLE ONLY public.appointment DROP CONSTRAINT appointment_pkey;
       public            postgres    false    224            �           2606    25778 0   appointment_treatment appointment_treatment_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.appointment_treatment
    ADD CONSTRAINT appointment_treatment_pkey PRIMARY KEY (appointment_treatment_id);
 Z   ALTER TABLE ONLY public.appointment_treatment DROP CONSTRAINT appointment_treatment_pkey;
       public            postgres    false    226            ~           2606    25731 "   medical_result medical_result_pkey 
   CONSTRAINT     o   ALTER TABLE ONLY public.medical_result
    ADD CONSTRAINT medical_result_pkey PRIMARY KEY (medical_result_id);
 L   ALTER TABLE ONLY public.medical_result DROP CONSTRAINT medical_result_pkey;
       public            postgres    false    218            |           2606    25723    patient patient_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.patient
    ADD CONSTRAINT patient_pkey PRIMARY KEY (patient_id);
 >   ALTER TABLE ONLY public.patient DROP CONSTRAINT patient_pkey;
       public            postgres    false    216            �           2606    25747    payment payment_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.payment
    ADD CONSTRAINT payment_pkey PRIMARY KEY (payment_id);
 >   ALTER TABLE ONLY public.payment DROP CONSTRAINT payment_pkey;
       public            postgres    false    222            �           2606    25739    treatment treatment_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.treatment
    ADD CONSTRAINT treatment_pkey PRIMARY KEY (treatment_id);
 B   ALTER TABLE ONLY public.treatment DROP CONSTRAINT treatment_pkey;
       public            postgres    false    220            �           2606    25795    users users_user_name_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_user_name_key UNIQUE (user_name);
 C   ALTER TABLE ONLY public.users DROP CONSTRAINT users_user_name_key;
       public            postgres    false    227            �           2606    25756 .   appointment appointment_medical_result_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_medical_result_id_fkey FOREIGN KEY (medical_result_id) REFERENCES public.medical_result(medical_result_id);
 X   ALTER TABLE ONLY public.appointment DROP CONSTRAINT appointment_medical_result_id_fkey;
       public          postgres    false    218    4734    224            �           2606    25761 '   appointment appointment_patient_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id);
 Q   ALTER TABLE ONLY public.appointment DROP CONSTRAINT appointment_patient_id_fkey;
       public          postgres    false    224    216    4732            �           2606    25766 '   appointment appointment_payment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payment(payment_id);
 Q   ALTER TABLE ONLY public.appointment DROP CONSTRAINT appointment_payment_id_fkey;
       public          postgres    false    224    4738    222            �           2606    25779 ?   appointment_treatment appointment_treatment_appointment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment_treatment
    ADD CONSTRAINT appointment_treatment_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES public.appointment(appointment_id);
 i   ALTER TABLE ONLY public.appointment_treatment DROP CONSTRAINT appointment_treatment_appointment_id_fkey;
       public          postgres    false    226    224    4740            �           2606    25784 =   appointment_treatment appointment_treatment_treatment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment_treatment
    ADD CONSTRAINT appointment_treatment_treatment_id_fkey FOREIGN KEY (treatment_id) REFERENCES public.treatment(treatment_id);
 g   ALTER TABLE ONLY public.appointment_treatment DROP CONSTRAINT appointment_treatment_treatment_id_fkey;
       public          postgres    false    226    220    4736            &      x������ � �      (      x������ � �             x������ � �            x������ � �      $      x������ � �      "      x�3����K��%\1z\\\ <��      )      x������ � �     