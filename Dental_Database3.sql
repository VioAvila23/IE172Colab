PGDMP      !                |            DentalStudio2    16.2    16.2 3    #           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            $           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            %           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            &           1262    17064    DentalStudio2    DATABASE     �   CREATE DATABASE "DentalStudio2" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
    DROP DATABASE "DentalStudio2";
                postgres    false            �            1259    17096    appointment    TABLE     �  CREATE TABLE public.appointment (
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
       public         heap    postgres    false            �            1259    17095    appointment_appointment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.appointment_appointment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.appointment_appointment_id_seq;
       public          postgres    false    224            '           0    0    appointment_appointment_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.appointment_appointment_id_seq OWNED BY public.appointment.appointment_id;
          public          postgres    false    223            �            1259    17118    appointment_treatment    TABLE     �   CREATE TABLE public.appointment_treatment (
    appointment_treatment_id integer NOT NULL,
    appointment_id integer,
    treatment_id integer,
    quantity integer NOT NULL,
    appointment_treatment_delete boolean DEFAULT false
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
       public          postgres    false    226            (           0    0 2   appointment_treatment_appointment_treatment_id_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public.appointment_treatment_appointment_treatment_id_seq OWNED BY public.appointment_treatment.appointment_treatment_id;
          public          postgres    false    225            �            1259    17075    medical_result    TABLE     (  CREATE TABLE public.medical_result (
    medical_result_id integer NOT NULL,
    medical_condition character varying(128) NOT NULL,
    medical_diagnosis character varying(128) NOT NULL,
    medical_prescription character varying(128) NOT NULL,
    medical_result_delete boolean DEFAULT false
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
       public          postgres    false    218            )           0    0 $   medical_result_medical_result_id_seq    SEQUENCE OWNED BY     m   ALTER SEQUENCE public.medical_result_medical_result_id_seq OWNED BY public.medical_result.medical_result_id;
          public          postgres    false    217            �            1259    17066    patient    TABLE     �  CREATE TABLE public.patient (
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
       public         heap    postgres    false            �            1259    17065    patient_patient_id_seq    SEQUENCE     �   CREATE SEQUENCE public.patient_patient_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.patient_patient_id_seq;
       public          postgres    false    216            *           0    0    patient_patient_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.patient_patient_id_seq OWNED BY public.patient.patient_id;
          public          postgres    false    215            �            1259    17089    payment    TABLE     1  CREATE TABLE public.payment (
    payment_id integer NOT NULL,
    payment_date date NOT NULL,
    payment_amount bigint NOT NULL,
    payment_status character varying(128) NOT NULL,
    paid_amount bigint NOT NULL,
    remarks character varying(128) NOT NULL,
    payment_delete boolean DEFAULT false
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
       public          postgres    false    222            +           0    0    payment_payment_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.payment_payment_id_seq OWNED BY public.payment.payment_id;
          public          postgres    false    221            �            1259    17082 	   treatment    TABLE       CREATE TABLE public.treatment (
    treatment_id integer NOT NULL,
    treatment_m character varying(128) NOT NULL,
    treatment_description character varying(128) NOT NULL,
    treatment_price integer NOT NULL,
    treatment_delete boolean DEFAULT false
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
       public          postgres    false    220            ,           0    0    treatment_treatment_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.treatment_treatment_id_seq OWNED BY public.treatment.treatment_id;
          public          postgres    false    219            q           2604    17099    appointment appointment_id    DEFAULT     �   ALTER TABLE ONLY public.appointment ALTER COLUMN appointment_id SET DEFAULT nextval('public.appointment_appointment_id_seq'::regclass);
 I   ALTER TABLE public.appointment ALTER COLUMN appointment_id DROP DEFAULT;
       public          postgres    false    223    224    224            s           2604    17121 .   appointment_treatment appointment_treatment_id    DEFAULT     �   ALTER TABLE ONLY public.appointment_treatment ALTER COLUMN appointment_treatment_id SET DEFAULT nextval('public.appointment_treatment_appointment_treatment_id_seq'::regclass);
 ]   ALTER TABLE public.appointment_treatment ALTER COLUMN appointment_treatment_id DROP DEFAULT;
       public          postgres    false    226    225    226            k           2604    17078     medical_result medical_result_id    DEFAULT     �   ALTER TABLE ONLY public.medical_result ALTER COLUMN medical_result_id SET DEFAULT nextval('public.medical_result_medical_result_id_seq'::regclass);
 O   ALTER TABLE public.medical_result ALTER COLUMN medical_result_id DROP DEFAULT;
       public          postgres    false    217    218    218            i           2604    17069    patient patient_id    DEFAULT     x   ALTER TABLE ONLY public.patient ALTER COLUMN patient_id SET DEFAULT nextval('public.patient_patient_id_seq'::regclass);
 A   ALTER TABLE public.patient ALTER COLUMN patient_id DROP DEFAULT;
       public          postgres    false    216    215    216            o           2604    17092    payment payment_id    DEFAULT     x   ALTER TABLE ONLY public.payment ALTER COLUMN payment_id SET DEFAULT nextval('public.payment_payment_id_seq'::regclass);
 A   ALTER TABLE public.payment ALTER COLUMN payment_id DROP DEFAULT;
       public          postgres    false    221    222    222            m           2604    17085    treatment treatment_id    DEFAULT     �   ALTER TABLE ONLY public.treatment ALTER COLUMN treatment_id SET DEFAULT nextval('public.treatment_treatment_id_seq'::regclass);
 E   ALTER TABLE public.treatment ALTER COLUMN treatment_id DROP DEFAULT;
       public          postgres    false    219    220    220                      0    17096    appointment 
   TABLE DATA           �   COPY public.appointment (appointment_id, medical_result_id, patient_id, payment_id, appointment_date, appointment_time, appointment_reason, appointment_status, appointment_delete) FROM stdin;
    public          postgres    false    224   4E                  0    17118    appointment_treatment 
   TABLE DATA           �   COPY public.appointment_treatment (appointment_treatment_id, appointment_id, treatment_id, quantity, appointment_treatment_delete) FROM stdin;
    public          postgres    false    226   aF                 0    17075    medical_result 
   TABLE DATA           �   COPY public.medical_result (medical_result_id, medical_condition, medical_diagnosis, medical_prescription, medical_result_delete) FROM stdin;
    public          postgres    false    218   �F                 0    17066    patient 
   TABLE DATA           �   COPY public.patient (patient_id, patient_last_m, patient_first_m, patient_middle_m, patient_bd, age, sex, patient_cn, patient_email, street, barangay, city, postal_code, account_creation_date, patient_delete) FROM stdin;
    public          postgres    false    216   �G                 0    17089    payment 
   TABLE DATA           �   COPY public.payment (payment_id, payment_date, payment_amount, payment_status, paid_amount, remarks, payment_delete) FROM stdin;
    public          postgres    false    222   "I                 0    17082 	   treatment 
   TABLE DATA           x   COPY public.treatment (treatment_id, treatment_m, treatment_description, treatment_price, treatment_delete) FROM stdin;
    public          postgres    false    220   �I       -           0    0    appointment_appointment_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.appointment_appointment_id_seq', 70, true);
          public          postgres    false    223            .           0    0 2   appointment_treatment_appointment_treatment_id_seq    SEQUENCE SET     a   SELECT pg_catalog.setval('public.appointment_treatment_appointment_treatment_id_seq', 13, true);
          public          postgres    false    225            /           0    0 $   medical_result_medical_result_id_seq    SEQUENCE SET     S   SELECT pg_catalog.setval('public.medical_result_medical_result_id_seq', 29, true);
          public          postgres    false    217            0           0    0    patient_patient_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.patient_patient_id_seq', 5, true);
          public          postgres    false    215            1           0    0    payment_payment_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.payment_payment_id_seq', 60, true);
          public          postgres    false    221            2           0    0    treatment_treatment_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.treatment_treatment_id_seq', 6, true);
          public          postgres    false    219            ~           2606    17101    appointment appointment_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_pkey PRIMARY KEY (appointment_id);
 F   ALTER TABLE ONLY public.appointment DROP CONSTRAINT appointment_pkey;
       public            postgres    false    224            �           2606    17123 0   appointment_treatment appointment_treatment_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.appointment_treatment
    ADD CONSTRAINT appointment_treatment_pkey PRIMARY KEY (appointment_treatment_id);
 Z   ALTER TABLE ONLY public.appointment_treatment DROP CONSTRAINT appointment_treatment_pkey;
       public            postgres    false    226            x           2606    17080 "   medical_result medical_result_pkey 
   CONSTRAINT     o   ALTER TABLE ONLY public.medical_result
    ADD CONSTRAINT medical_result_pkey PRIMARY KEY (medical_result_id);
 L   ALTER TABLE ONLY public.medical_result DROP CONSTRAINT medical_result_pkey;
       public            postgres    false    218            v           2606    17073    patient patient_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.patient
    ADD CONSTRAINT patient_pkey PRIMARY KEY (patient_id);
 >   ALTER TABLE ONLY public.patient DROP CONSTRAINT patient_pkey;
       public            postgres    false    216            |           2606    17094    payment payment_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.payment
    ADD CONSTRAINT payment_pkey PRIMARY KEY (payment_id);
 >   ALTER TABLE ONLY public.payment DROP CONSTRAINT payment_pkey;
       public            postgres    false    222            z           2606    17087    treatment treatment_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.treatment
    ADD CONSTRAINT treatment_pkey PRIMARY KEY (treatment_id);
 B   ALTER TABLE ONLY public.treatment DROP CONSTRAINT treatment_pkey;
       public            postgres    false    220            �           2606    17102 .   appointment appointment_medical_result_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_medical_result_id_fkey FOREIGN KEY (medical_result_id) REFERENCES public.medical_result(medical_result_id);
 X   ALTER TABLE ONLY public.appointment DROP CONSTRAINT appointment_medical_result_id_fkey;
       public          postgres    false    224    4728    218            �           2606    17107 '   appointment appointment_patient_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id);
 Q   ALTER TABLE ONLY public.appointment DROP CONSTRAINT appointment_patient_id_fkey;
       public          postgres    false    224    216    4726            �           2606    17112 '   appointment appointment_payment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payment(payment_id);
 Q   ALTER TABLE ONLY public.appointment DROP CONSTRAINT appointment_payment_id_fkey;
       public          postgres    false    224    222    4732            �           2606    17124 ?   appointment_treatment appointment_treatment_appointment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment_treatment
    ADD CONSTRAINT appointment_treatment_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES public.appointment(appointment_id);
 i   ALTER TABLE ONLY public.appointment_treatment DROP CONSTRAINT appointment_treatment_appointment_id_fkey;
       public          postgres    false    4734    224    226            �           2606    17129 =   appointment_treatment appointment_treatment_treatment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointment_treatment
    ADD CONSTRAINT appointment_treatment_treatment_id_fkey FOREIGN KEY (treatment_id) REFERENCES public.treatment(treatment_id);
 g   ALTER TABLE ONLY public.appointment_treatment DROP CONSTRAINT appointment_treatment_treatment_id_fkey;
       public          postgres    false    220    4730    226                 x�}��n�0���S�R�k��1z�*�c.�	
1Qp����Mq���7;c[������� x!y�9T�`�l$=v��:��p��d���a�/�ڈ"V�,�us��� ��H�����y��-��ۙ]�N�+��+�a��\�P���}��{�����
D��wKb����u˚?s&	��a�D�f����S�Wk=�A`��j#��D�W *� T�$�E��p"�*yt'���$�z­6�u�\�>��o����0���6�+)�rZN.9+����OQ}�          I   x�-��� ��3L�!��o��q�s���r�C����-D�"�w3jȆ��&e���*=�Z=9���<g�         
  x���An� E��Sp���nӬ%�Jɲ�0��8��Kp\�V�*z��K8X4ۣ��L�
3#�A��t�E���M����o��apM�OT�
��%<�IȚ�W�n�؆<
����ެ�C�[�4^H�A��!�Qx[jhDorT(���`)\N���	��<\z�3)�b�G�����,AZ�(����X���t��*�/U�x߱���iE|���q���9c��g�2���|�1��5����Y�ۏ��(�����         >  x����N�0�ϓ��8�����G��^���eBkp�*)������Ǖf���%��]��+�^�T�$��D0+v5J�&I��H�Q�68&�7{WǕo@:3�U;�9`��[>�s{8�P��҉$��5�x��YnzLۖ1䢐*���dX�͈���,��5��I���i���^���U�1�����ڙT������������4B�����:�KPv�N���`���߅�3�HUJ*a�O��E7�����}�Q��C�[P~� ��h��z��w�W>(�χ�k=��8Z�g�6�m�����&@��(�~ �A��         �   x�m�A!E����ZA=�k�	�!A4s��@��q�ڼ�~�l&�I�Zk�Ip����-�ӧ��Z`�U+��f�0]5��POpnr	�5�-|r!=v!�Cd���n����+c�^J�%9������Z�AC         �   x�5O�N1<;_�[oh�>����
.\��ӍH�*�Ov#.��=�w�=Ec�r��M���x+�y���0�3�>�X���`���_�Tm��ԋ|���HB�v��V�,�#�ڕ{�ba.�[��&F�ښE_�d�0�������x�7���ղ�o*ֹ�hƑ2]�C�:����ǔ*^���>U����<9�� �]~     