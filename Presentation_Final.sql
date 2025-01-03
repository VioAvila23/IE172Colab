PGDMP  4    5                |            DDDD    16.2    16.2 6    ,           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            -           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            .           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            /           1262    25924    DDDD    DATABASE     �   CREATE DATABASE "DDDD" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
    DROP DATABASE "DDDD";
                postgres    false            �            1259    25925    appointment    TABLE     �  CREATE TABLE public.appointment (
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
       public         heap    postgres    false            �            1259    25929    appointment_appointment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.appointment_appointment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.appointment_appointment_id_seq;
       public          postgres    false    215            0           0    0    appointment_appointment_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.appointment_appointment_id_seq OWNED BY public.appointment.appointment_id;
          public          postgres    false    216            �            1259    25930    appointment_treatment    TABLE     �   CREATE TABLE public.appointment_treatment (
    appointment_treatment_id integer NOT NULL,
    appointment_id integer,
    treatment_id integer,
    quantity integer NOT NULL,
    appointment_treatment_delete boolean DEFAULT false
);
 )   DROP TABLE public.appointment_treatment;
       public         heap    postgres    false            �            1259    25934 2   appointment_treatment_appointment_treatment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.appointment_treatment_appointment_treatment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 I   DROP SEQUENCE public.appointment_treatment_appointment_treatment_id_seq;
       public          postgres    false    217            1           0    0 2   appointment_treatment_appointment_treatment_id_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public.appointment_treatment_appointment_treatment_id_seq OWNED BY public.appointment_treatment.appointment_treatment_id;
          public          postgres    false    218            �            1259    25935    medical_result    TABLE     (  CREATE TABLE public.medical_result (
    medical_result_id integer NOT NULL,
    medical_condition character varying(128) NOT NULL,
    medical_diagnosis character varying(128) NOT NULL,
    medical_prescription character varying(128) NOT NULL,
    medical_result_delete boolean DEFAULT false
);
 "   DROP TABLE public.medical_result;
       public         heap    postgres    false            �            1259    25939 $   medical_result_medical_result_id_seq    SEQUENCE     �   CREATE SEQUENCE public.medical_result_medical_result_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE public.medical_result_medical_result_id_seq;
       public          postgres    false    219            2           0    0 $   medical_result_medical_result_id_seq    SEQUENCE OWNED BY     m   ALTER SEQUENCE public.medical_result_medical_result_id_seq OWNED BY public.medical_result.medical_result_id;
          public          postgres    false    220            �            1259    25940    patient    TABLE     �  CREATE TABLE public.patient (
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
       public         heap    postgres    false            �            1259    25946    patient_patient_id_seq    SEQUENCE     �   CREATE SEQUENCE public.patient_patient_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.patient_patient_id_seq;
       public          postgres    false    221            3           0    0    patient_patient_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.patient_patient_id_seq OWNED BY public.patient.patient_id;
          public          postgres    false    222            �            1259    25947    payment    TABLE     1  CREATE TABLE public.payment (
    payment_id integer NOT NULL,
    payment_date date NOT NULL,
    payment_amount bigint NOT NULL,
    payment_status character varying(128) NOT NULL,
    paid_amount bigint NOT NULL,
    remarks character varying(128) NOT NULL,
    payment_delete boolean DEFAULT false
);
    DROP TABLE public.payment;
       public         heap    postgres    false            �            1259    25951    payment_payment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.payment_payment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.payment_payment_id_seq;
       public          postgres    false    223            4           0    0    payment_payment_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.payment_payment_id_seq OWNED BY public.payment.payment_id;
          public          postgres    false    224            �            1259    25952 	   treatment    TABLE       CREATE TABLE public.treatment (
    treatment_id integer NOT NULL,
    treatment_m character varying(128) NOT NULL,
    treatment_description character varying(128) NOT NULL,
    treatment_price integer NOT NULL,
    treatment_delete boolean DEFAULT false
);
    DROP TABLE public.treatment;
       public         heap    postgres    false            �            1259    25956    treatment_treatment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.treatment_treatment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.treatment_treatment_id_seq;
       public          postgres    false    225            5           0    0    treatment_treatment_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.treatment_treatment_id_seq OWNED BY public.treatment.treatment_id;
          public          postgres    false    226            �            1259    25957    users    TABLE     �   CREATE TABLE public.users (
    user_name character varying(32),
    user_password character varying(64) NOT NULL,
    user_modified_on timestamp without time zone DEFAULT now(),
    user_delete_ind boolean DEFAULT false
);
    DROP TABLE public.users;
       public         heap    postgres    false            m           2604    25962    appointment appointment_id    DEFAULT     �   ALTER TABLE ONLY public.appointment ALTER COLUMN appointment_id SET DEFAULT nextval('public.appointment_appointment_id_seq'::regclass);
 I   ALTER TABLE public.appointment ALTER COLUMN appointment_id DROP DEFAULT;
       public          postgres    false    216    215            o           2604    25963 .   appointment_treatment appointment_treatment_id    DEFAULT     �   ALTER TABLE ONLY public.appointment_treatment ALTER COLUMN appointment_treatment_id SET DEFAULT nextval('public.appointment_treatment_appointment_treatment_id_seq'::regclass);
 ]   ALTER TABLE public.appointment_treatment ALTER COLUMN appointment_treatment_id DROP DEFAULT;
       public          postgres    false    218    217            q           2604    25964     medical_result medical_result_id    DEFAULT     �   ALTER TABLE ONLY public.medical_result ALTER COLUMN medical_result_id SET DEFAULT nextval('public.medical_result_medical_result_id_seq'::regclass);
 O   ALTER TABLE public.medical_result ALTER COLUMN medical_result_id DROP DEFAULT;
       public          postgres    false    220    219            s           2604    25965    patient patient_id    DEFAULT     x   ALTER TABLE ONLY public.patient ALTER COLUMN patient_id SET DEFAULT nextval('public.patient_patient_id_seq'::regclass);
 A   ALTER TABLE public.patient ALTER COLUMN patient_id DROP DEFAULT;
       public          postgres    false    222    221            u           2604    25966    payment payment_id    DEFAULT     x   ALTER TABLE ONLY public.payment ALTER COLUMN payment_id SET DEFAULT nextval('public.payment_payment_id_seq'::regclass);
 A   ALTER TABLE public.payment ALTER COLUMN payment_id DROP DEFAULT;
       public          postgres    false    224    223            w           2604    25967    treatment treatment_id    DEFAULT     �   ALTER TABLE ONLY public.treatment ALTER COLUMN treatment_id SET DEFAULT nextval('public.treatment_treatment_id_seq'::regclass);
 E   ALTER TABLE public.treatment ALTER COLUMN treatment_id DROP DEFAULT;
       public          postgres    false    226    225                      0    25925    appointment 
   TABLE DATA           �   COPY public.appointment (appointment_id, medical_result_id, patient_id, payment_id, appointment_date, appointment_time, appointment_reason, appointment_status, appointment_delete) FROM stdin;
    public          postgres    false    215   {H                 0    25930    appointment_treatment 
   TABLE DATA           �   COPY public.appointment_treatment (appointment_treatment_id, appointment_id, treatment_id, quantity, appointment_treatment_delete) FROM stdin;
    public          postgres    false    217   7I       !          0    25935    medical_result 
   TABLE DATA           �   COPY public.medical_result (medical_result_id, medical_condition, medical_diagnosis, medical_prescription, medical_result_delete) FROM stdin;
    public          postgres    false    219   �I       #          0    25940    patient 
   TABLE DATA           �   COPY public.patient (patient_id, patient_last_m, patient_first_m, patient_middle_m, patient_bd, age, sex, patient_cn, patient_email, street, barangay, city, postal_code, account_creation_date, patient_delete) FROM stdin;
    public          postgres    false    221   |J       %          0    25947    payment 
   TABLE DATA           �   COPY public.payment (payment_id, payment_date, payment_amount, payment_status, paid_amount, remarks, payment_delete) FROM stdin;
    public          postgres    false    223   �K       '          0    25952 	   treatment 
   TABLE DATA           x   COPY public.treatment (treatment_id, treatment_m, treatment_description, treatment_price, treatment_delete) FROM stdin;
    public          postgres    false    225   �L       )          0    25957    users 
   TABLE DATA           \   COPY public.users (user_name, user_password, user_modified_on, user_delete_ind) FROM stdin;
    public          postgres    false    227   �M       6           0    0    appointment_appointment_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.appointment_appointment_id_seq', 4, true);
          public          postgres    false    216            7           0    0 2   appointment_treatment_appointment_treatment_id_seq    SEQUENCE SET     a   SELECT pg_catalog.setval('public.appointment_treatment_appointment_treatment_id_seq', 20, true);
          public          postgres    false    218            8           0    0 $   medical_result_medical_result_id_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('public.medical_result_medical_result_id_seq', 4, true);
          public          postgres    false    220            9           0    0    patient_patient_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.patient_patient_id_seq', 4, true);
          public          postgres    false    222            :           0    0    payment_payment_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.payment_payment_id_seq', 4, true);
          public          postgres    false    224            ;           0    0    treatment_treatment_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.treatment_treatment_id_seq', 10, true);
          public          postgres    false    226            |           2606    25969    appointment appointment_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_pkey PRIMARY KEY (appointment_id);
 F   ALTER TABLE ONLY public.appointment DROP CONSTRAINT appointment_pkey;
       public            postgres    false    215            ~           2606    25971 0   appointment_treatment appointment_treatment_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.appointment_treatment
    ADD CONSTRAINT appointment_treatment_pkey PRIMARY KEY (appointment_treatment_id);
 Z   ALTER TABLE ONLY public.appointment_treatment DROP CONSTRAINT appointment_treatment_pkey;
       public            postgres    false    217            �           2606    25973 "   medical_result medical_result_pkey 
   CONSTRAINT     o   ALTER TABLE ONLY public.medical_result
    ADD CONSTRAINT medical_result_pkey PRIMARY KEY (medical_result_id);
 L   ALTER TABLE ONLY public.medical_result DROP CONSTRAINT medical_result_pkey;
       public            postgres    false    219            �           2606    25975    patient patient_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.patient
    ADD CONSTRAINT patient_pkey PRIMARY KEY (patient_id);
 >   ALTER TABLE ONLY public.patient DROP CONSTRAINT patient_pkey;
       public            postgres    false    221            �           2606    25977    payment payment_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.payment
    ADD CONSTRAINT payment_pkey PRIMARY KEY (payment_id);
 >   ALTER TABLE ONLY public.payment DROP CONSTRAINT payment_pkey;
       public            postgres    false    223            �           2606    25979    treatment treatment_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.treatment
    ADD CONSTRAINT treatment_pkey PRIMARY KEY (treatment_id);
 B   ALTER TABLE ONLY public.treatment DROP CONSTRAINT treatment_pkey;
       public            postgres    false    225            �           2606    25981    users users_user_name_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_user_name_key UNIQUE (user_name);
 C   ALTER TABLE ONLY public.users DROP CONSTRAINT users_user_name_key;
       public            postgres    false    227            �           2606    25982 .   appointment appointment_medical_result_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_medical_result_id_fkey FOREIGN KEY (medical_result_id) REFERENCES public.medical_result(medical_result_id);
 X   ALTER TABLE ONLY public.appointment DROP CONSTRAINT appointment_medical_result_id_fkey;
       public          postgres    false    4736    215    219            �           2606    25987 '   appointment appointment_patient_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id);
 Q   ALTER TABLE ONLY public.appointment DROP CONSTRAINT appointment_patient_id_fkey;
       public          postgres    false    4738    215    221            �           2606    25992 '   appointment appointment_payment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payment(payment_id);
 Q   ALTER TABLE ONLY public.appointment DROP CONSTRAINT appointment_payment_id_fkey;
       public          postgres    false    4740    215    223            �           2606    25997 ?   appointment_treatment appointment_treatment_appointment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment_treatment
    ADD CONSTRAINT appointment_treatment_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES public.appointment(appointment_id);
 i   ALTER TABLE ONLY public.appointment_treatment DROP CONSTRAINT appointment_treatment_appointment_id_fkey;
       public          postgres    false    215    217    4732            �           2606    26002 =   appointment_treatment appointment_treatment_treatment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment_treatment
    ADD CONSTRAINT appointment_treatment_treatment_id_fkey FOREIGN KEY (treatment_id) REFERENCES public.treatment(treatment_id);
 g   ALTER TABLE ONLY public.appointment_treatment DROP CONSTRAINT appointment_treatment_treatment_id_fkey;
       public          postgres    false    4742    217    225               �   x�U�M
�0�����@d�S��
@\��ij1S�=�i�B������Fm�B�k���u�"�e�O��3d�=�8t�WL���ڴ��3�Do9���I��u�9zq���]H�^2[i�-�%t-+>\G�;�`�T5(ln�g�9���./�\����CUU_��F�         _   x�E���0г�
��v���P'D��I	��q>1fY�̱�̺T�*fs�Q��TlǑ�KEF�>�L�_��
�a�Nƣ:��Z:|�őd      !   �   x�M��N�0D����P)�%�*�H������+�m��C�{z�6�Ѽ�G�h�"lpι|cO?x*41�`�M��J�6N�������0�$M�B5b�F��HN��s��\%1���MZ�	1R�_��\��{�֚�)�a�3y6|_H�9�g8����m��_tl��ݧ"�E�m��ԯ9��>�s���VD      #   O  x�u��N�0��O��i�s�qqɜ^zs�*�A1L��=�48�U/����|�p�dk���m��#ڦ�A�i���
T
RK��"�wJ��Ի�%����L�{l���Сͱc�,����U��꾲lm���P!�2�WO�Aw��Ig6�tM��W^�<*�x(�0wCqFCWl��S����S�p�l�o�6��f!�o���Gf�V0zRB_D��@�7A:��P�I^��M��l��GOFG�o�?�36�£�yhN�S�#,-®��=�I�1  ���g��"/��'P�m�,X�ó¼-_���9�LH�5�3�<��8�_      %   �   x�u�1�0��~�-�4�b���n�G����T��TAqp���ӷid�ɒ�$�:ʴ����V_�x(�������*���E)���rUQ�9�n^������7�������+8N�GnZ�r�sޘ�v\j���-v7'��aṑ�P*v��� g?�&|?o��9LhG�QA���`�:�;��8~hpe�      '   C  x�U��N�0���S�����8��M�؁KH��R�T�;���M�IHU��������;�G	\T����U�E�ȝ�3�c$�ʈ�)3��eYB[,��Էڰ<�=��,�o�v�\���Q<���*a�pH�:bL�j{d27�߹�"�3'�	�2H�z�t���p���ՠ��YS9#l2��� �D�����{0�,�򩐓@�M��������$�>�ķ�.ƀ�MB7�ʝo��"���ѲN�ڊ�iΏ�2�\%��T�����5�^�����{��� �։����q��W8.��*��i���6�8N�s�(� �T��      )   ^   x����0�Z�"�����,idYR$�������k�s!L��}xo��Ž1\!�������f���JCY;X��R��OѪ�����,�     