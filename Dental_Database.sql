PGDMP      :                |            DentalStudio2    16.2    16.2 3               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                        1262    17064    DentalStudio2    DATABASE     �   CREATE DATABASE "DentalStudio2" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
    DROP DATABASE "DentalStudio2";
                postgres    false            �            1259    17096    appointment    TABLE     b  CREATE TABLE public.appointment (
    appointment_id integer NOT NULL,
    medical_result_id integer,
    patient_id integer,
    payment_id integer,
    appointment_date date NOT NULL,
    appointment_time time without time zone NOT NULL,
    appointment_reason character varying(128) NOT NULL,
    appointment_status character varying(128) NOT NULL
);
    DROP TABLE public.appointment;
       public         heap    postgres    false            �            1259    17095    appointment_appointment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.appointment_appointment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.appointment_appointment_id_seq;
       public          postgres    false    224            !           0    0    appointment_appointment_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.appointment_appointment_id_seq OWNED BY public.appointment.appointment_id;
          public          postgres    false    223            �            1259    17118    appointment_treatment    TABLE     �   CREATE TABLE public.appointment_treatment (
    appointment_treatment_id integer NOT NULL,
    appointment_id integer,
    treatment_id integer,
    quantity integer NOT NULL
);
 )   DROP TABLE public.appointment_treatment;
       public         heap    postgres    false            �            1259    17117 2   appointment_treatment_appointment_treatment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.appointment_treatment_appointment_treatment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 I   DROP SEQUENCE public.appointment_treatment_appointment_treatment_id_seq;
       public          postgres    false    226            "           0    0 2   appointment_treatment_appointment_treatment_id_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public.appointment_treatment_appointment_treatment_id_seq OWNED BY public.appointment_treatment.appointment_treatment_id;
          public          postgres    false    225            �            1259    17075    medical_result    TABLE     �   CREATE TABLE public.medical_result (
    medical_result_id integer NOT NULL,
    medical_condition character varying(128) NOT NULL,
    medical_diagnosis character varying(128) NOT NULL,
    medical_prescription character varying(128) NOT NULL
);
 "   DROP TABLE public.medical_result;
       public         heap    postgres    false            �            1259    17074 $   medical_result_medical_result_id_seq    SEQUENCE     �   CREATE SEQUENCE public.medical_result_medical_result_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE public.medical_result_medical_result_id_seq;
       public          postgres    false    218            #           0    0 $   medical_result_medical_result_id_seq    SEQUENCE OWNED BY     m   ALTER SEQUENCE public.medical_result_medical_result_id_seq OWNED BY public.medical_result.medical_result_id;
          public          postgres    false    217            �            1259    17066    patient    TABLE     Z  CREATE TABLE public.patient (
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
    account_creation_date date NOT NULL
);
    DROP TABLE public.patient;
       public         heap    postgres    false            �            1259    17065    patient_patient_id_seq    SEQUENCE     �   CREATE SEQUENCE public.patient_patient_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.patient_patient_id_seq;
       public          postgres    false    216            $           0    0    patient_patient_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.patient_patient_id_seq OWNED BY public.patient.patient_id;
          public          postgres    false    215            �            1259    17089    payment    TABLE       CREATE TABLE public.payment (
    payment_id integer NOT NULL,
    payment_date date NOT NULL,
    payment_amount bigint NOT NULL,
    payment_status character varying(128) NOT NULL,
    paid_amount bigint NOT NULL,
    remarks character varying(128) NOT NULL
);
    DROP TABLE public.payment;
       public         heap    postgres    false            �            1259    17088    payment_payment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.payment_payment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.payment_payment_id_seq;
       public          postgres    false    222            %           0    0    payment_payment_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.payment_payment_id_seq OWNED BY public.payment.payment_id;
          public          postgres    false    221            �            1259    17082 	   treatment    TABLE     �   CREATE TABLE public.treatment (
    treatment_id integer NOT NULL,
    treatment_m character varying(128) NOT NULL,
    treatment_description character varying(128) NOT NULL,
    treatment_price integer NOT NULL
);
    DROP TABLE public.treatment;
       public         heap    postgres    false            �            1259    17081    treatment_treatment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.treatment_treatment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.treatment_treatment_id_seq;
       public          postgres    false    220            &           0    0    treatment_treatment_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.treatment_treatment_id_seq OWNED BY public.treatment.treatment_id;
          public          postgres    false    219            m           2604    17099    appointment appointment_id    DEFAULT     �   ALTER TABLE ONLY public.appointment ALTER COLUMN appointment_id SET DEFAULT nextval('public.appointment_appointment_id_seq'::regclass);
 I   ALTER TABLE public.appointment ALTER COLUMN appointment_id DROP DEFAULT;
       public          postgres    false    223    224    224            n           2604    17121 .   appointment_treatment appointment_treatment_id    DEFAULT     �   ALTER TABLE ONLY public.appointment_treatment ALTER COLUMN appointment_treatment_id SET DEFAULT nextval('public.appointment_treatment_appointment_treatment_id_seq'::regclass);
 ]   ALTER TABLE public.appointment_treatment ALTER COLUMN appointment_treatment_id DROP DEFAULT;
       public          postgres    false    225    226    226            j           2604    17078     medical_result medical_result_id    DEFAULT     �   ALTER TABLE ONLY public.medical_result ALTER COLUMN medical_result_id SET DEFAULT nextval('public.medical_result_medical_result_id_seq'::regclass);
 O   ALTER TABLE public.medical_result ALTER COLUMN medical_result_id DROP DEFAULT;
       public          postgres    false    218    217    218            i           2604    17069    patient patient_id    DEFAULT     x   ALTER TABLE ONLY public.patient ALTER COLUMN patient_id SET DEFAULT nextval('public.patient_patient_id_seq'::regclass);
 A   ALTER TABLE public.patient ALTER COLUMN patient_id DROP DEFAULT;
       public          postgres    false    216    215    216            l           2604    17092    payment payment_id    DEFAULT     x   ALTER TABLE ONLY public.payment ALTER COLUMN payment_id SET DEFAULT nextval('public.payment_payment_id_seq'::regclass);
 A   ALTER TABLE public.payment ALTER COLUMN payment_id DROP DEFAULT;
       public          postgres    false    222    221    222            k           2604    17085    treatment treatment_id    DEFAULT     �   ALTER TABLE ONLY public.treatment ALTER COLUMN treatment_id SET DEFAULT nextval('public.treatment_treatment_id_seq'::regclass);
 E   ALTER TABLE public.treatment ALTER COLUMN treatment_id DROP DEFAULT;
       public          postgres    false    220    219    220                      0    17096    appointment 
   TABLE DATA           �   COPY public.appointment (appointment_id, medical_result_id, patient_id, payment_id, appointment_date, appointment_time, appointment_reason, appointment_status) FROM stdin;
    public          postgres    false    224   �C                 0    17118    appointment_treatment 
   TABLE DATA           q   COPY public.appointment_treatment (appointment_treatment_id, appointment_id, treatment_id, quantity) FROM stdin;
    public          postgres    false    226   UD                 0    17075    medical_result 
   TABLE DATA           w   COPY public.medical_result (medical_result_id, medical_condition, medical_diagnosis, medical_prescription) FROM stdin;
    public          postgres    false    218   �D                 0    17066    patient 
   TABLE DATA           �   COPY public.patient (patient_id, patient_last_m, patient_first_m, patient_middle_m, patient_bd, age, sex, patient_cn, patient_email, street, barangay, city, postal_code, account_creation_date) FROM stdin;
    public          postgres    false    216   YE                 0    17089    payment 
   TABLE DATA           q   COPY public.payment (payment_id, payment_date, payment_amount, payment_status, paid_amount, remarks) FROM stdin;
    public          postgres    false    222   yF                 0    17082 	   treatment 
   TABLE DATA           f   COPY public.treatment (treatment_id, treatment_m, treatment_description, treatment_price) FROM stdin;
    public          postgres    false    220   G       '           0    0    appointment_appointment_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.appointment_appointment_id_seq', 8, true);
          public          postgres    false    223            (           0    0 2   appointment_treatment_appointment_treatment_id_seq    SEQUENCE SET     `   SELECT pg_catalog.setval('public.appointment_treatment_appointment_treatment_id_seq', 8, true);
          public          postgres    false    225            )           0    0 $   medical_result_medical_result_id_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('public.medical_result_medical_result_id_seq', 7, true);
          public          postgres    false    217            *           0    0    patient_patient_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.patient_patient_id_seq', 4, true);
          public          postgres    false    215            +           0    0    payment_payment_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.payment_payment_id_seq', 5, true);
          public          postgres    false    221            ,           0    0    treatment_treatment_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.treatment_treatment_id_seq', 4, true);
          public          postgres    false    219            x           2606    17101    appointment appointment_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_pkey PRIMARY KEY (appointment_id);
 F   ALTER TABLE ONLY public.appointment DROP CONSTRAINT appointment_pkey;
       public            postgres    false    224            z           2606    17123 0   appointment_treatment appointment_treatment_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.appointment_treatment
    ADD CONSTRAINT appointment_treatment_pkey PRIMARY KEY (appointment_treatment_id);
 Z   ALTER TABLE ONLY public.appointment_treatment DROP CONSTRAINT appointment_treatment_pkey;
       public            postgres    false    226            r           2606    17080 "   medical_result medical_result_pkey 
   CONSTRAINT     o   ALTER TABLE ONLY public.medical_result
    ADD CONSTRAINT medical_result_pkey PRIMARY KEY (medical_result_id);
 L   ALTER TABLE ONLY public.medical_result DROP CONSTRAINT medical_result_pkey;
       public            postgres    false    218            p           2606    17073    patient patient_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.patient
    ADD CONSTRAINT patient_pkey PRIMARY KEY (patient_id);
 >   ALTER TABLE ONLY public.patient DROP CONSTRAINT patient_pkey;
       public            postgres    false    216            v           2606    17094    payment payment_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.payment
    ADD CONSTRAINT payment_pkey PRIMARY KEY (payment_id);
 >   ALTER TABLE ONLY public.payment DROP CONSTRAINT payment_pkey;
       public            postgres    false    222            t           2606    17087    treatment treatment_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.treatment
    ADD CONSTRAINT treatment_pkey PRIMARY KEY (treatment_id);
 B   ALTER TABLE ONLY public.treatment DROP CONSTRAINT treatment_pkey;
       public            postgres    false    220            {           2606    17102 .   appointment appointment_medical_result_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_medical_result_id_fkey FOREIGN KEY (medical_result_id) REFERENCES public.medical_result(medical_result_id);
 X   ALTER TABLE ONLY public.appointment DROP CONSTRAINT appointment_medical_result_id_fkey;
       public          postgres    false    4722    218    224            |           2606    17107 '   appointment appointment_patient_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id);
 Q   ALTER TABLE ONLY public.appointment DROP CONSTRAINT appointment_patient_id_fkey;
       public          postgres    false    224    4720    216            }           2606    17112 '   appointment appointment_payment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payment(payment_id);
 Q   ALTER TABLE ONLY public.appointment DROP CONSTRAINT appointment_payment_id_fkey;
       public          postgres    false    4726    222    224            ~           2606    17124 ?   appointment_treatment appointment_treatment_appointment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment_treatment
    ADD CONSTRAINT appointment_treatment_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES public.appointment(appointment_id);
 i   ALTER TABLE ONLY public.appointment_treatment DROP CONSTRAINT appointment_treatment_appointment_id_fkey;
       public          postgres    false    224    226    4728                       2606    17129 =   appointment_treatment appointment_treatment_treatment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment_treatment
    ADD CONSTRAINT appointment_treatment_treatment_id_fkey FOREIGN KEY (treatment_id) REFERENCES public.treatment(treatment_id);
 g   ALTER TABLE ONLY public.appointment_treatment DROP CONSTRAINT appointment_treatment_treatment_id_fkey;
       public          postgres    false    226    4724    220               �   x�u���0E�ׯ�`�J����G���H#"�Ŀ�@������{p�Re(3���E!��>4|$?���.|�컡�@�IH�y��g�|��I��ه�n�NmtrX�9�9
�s�:>��J�:�`
�lp�\�e��|�c��wX�Wi?�@�oy�g����}�F�         +   x�3�4A.#N4�2�AC.N0ߜ�,o�A�=... ��K         �   x�u��n1���S�	*�"� ��k�r�b%������B��e%�wٟ=3��l�ߐ��~��i�`,R�:M�4�n�Q��=ߏ�E��\�;��Ыh�N��A����^h3��j�T����f�����qҠ	��������lr�r�u7��yV�˰��s�q���H�o��+<�ǿ[힜s}�x�           x�eнN�0���~G��N�lЈ!�$+X�!�S��q�.��ҝ>��8O#����T�ą�DP
[�;�$�.��b(_7������4��f+�=k�X�`ǝ=��?��H)��$��ċ�{o���h���1\h.T��������ZJh]Tlk�)�˅^���V���y�Ɔ~��x�\ra8����
�%��.��j��fCW��)�����G��v:���δ��TCѿ��%��b��B��>�t�Y�{P���y�e��&�w         �   x�e�A!�u9E/0�Ԣ���p�4$���bn��w���RL,���I����L	��B��'t��[��2�d@���	w��_�5�[�����:*nT��������^����M5{ds�c^Ь?         �   x�5��N1Dk�+��C����!hh���6b����>�ET�g�x|/KvZ���������n5r���8M�Nέ^M�i�+�H���3�V_��N�:g5]�����7��qB�v߃���&/e����>��ء6#m=WCMP��W�pF?"G�MG�Z�H�Vf-z�O{��m���O�     