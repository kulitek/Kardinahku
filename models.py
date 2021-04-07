from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, CHAR
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    is_active = Column(Boolean, default=False)
    role = Column(String, default='user')
    id_pegawai = Column(String(11), ForeignKey("pegawai.id"))
    token = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)

    pegawai = relationship("Pegawai", back_populates="user")
    # masalah_lv1 = relationship("Masalah", back_populates="disposisi_1")
    # masalah_lv2 = relationship("Masalah", back_populates="disposisi_2")
    # masalah_lv3 = relationship("Masalah", back_populates="disposisi_3")


class Pegawai(Base):
    __tablename__ = "pegawai"

    id = Column(String(11), primary_key=True, index=True)
    nama_lengkap = Column(String(60))
    nama_panggilan = Column(String(60), nullable=True)
    tempat_lahir = Column(String(20), nullable=True)
    tanggal_lahir = Column(DateTime, nullable=True)
    jenis_kelamin = Column(CHAR(1), default='L')
    no_hp = Column(String(16), nullable=True)
    no_wa = Column(String(16), nullable=True)

    created_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="pegawai")


class KategoriMasalah(Base):
    __tablename__ = "kategori_masalah"

    id = Column(Integer, primary_key=True, index=True)
    kategori = Column(String(60))

    masalah = relationship("Masalah", back_populates="kategori_masalah")

class KategoriTindakan(Base):
    __tablename__ = "kategori_tindakan"

    id = Column(Integer, primary_key=True, index=True)
    kategori = Column(String(50))

    tindakan = relationship("Tindakan", back_populates="kategori_tindakan")


class Instalasi(Base):
    __tablename__ = "instalasi"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(40))

    ruangan = relationship("Ruangan", back_populates="instalasi")


class Ruangan(Base):
    __tablename__ = "ruangan"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(60))
    id_instalasi = Column(Integer, ForeignKey("instalasi.id"))

    instalasi = relationship("Instalasi", back_populates="ruangan")
    masalah = relationship("Masalah", back_populates="ruangan")
    sarana = relationship("Sarana", back_populates="ruangan")
    tindakan = relationship("Tindakan", back_populates="ruangan")

class JenisSarana(Base):
    __tablename__ = "jenis_sarana"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(30))

    created_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)

    sarana = relationship("Sarana", back_populates="jenis")


class Sarana(Base):
    __tablename__ = "sarana"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(90))
    berat = Column(String(30), nullable=True)
    panjang = Column(String(30), nullable=True)
    lebar = Column(String(30), nullable=True)
    tinggi = Column(String(30), nullable=True)
    foto = Column(String, nullable=True)
    id_ruangan = Column(Integer, ForeignKey("ruangan.id"), nullable=True)
    id_jenis = Column(Integer, ForeignKey("jenis_sarana.id"))

    created_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)

    masalah = relationship("Masalah", back_populates="sarana")
    ruangan = relationship("Ruangan", back_populates="sarana")
    tindakan = relationship("Tindakan", back_populates="sarana")
    jenis = relationship("JenisSarana", back_populates="sarana")
    # id_kamar = Column(Integer, ForeignKey(""))



class Masalah(Base):
    __tablename__ = "masalah"

    id = Column(Integer, primary_key=True, index=True)
    deskripsi = Column(Text)
    id_user = Column(Integer, ForeignKey("users.id"), nullable=True)
    id_kategori_masalah = Column(Integer, ForeignKey("kategori_masalah.id"), nullable=True)
    id_ruangan = Column(Integer, ForeignKey("ruangan.id"), nullable=True)
    id_sarana = Column(Integer, ForeignKey("sarana.id"), nullable=True)
    id_level_1 = Column(Integer, nullable=True)
    id_level_2 = Column(Integer, nullable=True)
    id_level_3 = Column(Integer, nullable=True)
    status = Column(Boolean, default=False)
    foto = Column(String, nullable=True)


    created_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    done_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    kategori_masalah = relationship("KategoriMasalah", back_populates="masalah")
    ruangan = relationship("Ruangan", back_populates="masalah")
    sarana = relationship("Sarana", back_populates="masalah")
    tindakan = relationship("Tindakan", back_populates="masalah")
    # disposisi_1 = relationship("User", back_populates="masalah_lv1")
    # disposisi_2 = relationship("User", back_populates="masalah_lv2")
    # disposisi_3 = relationship("User", back_populates="masalah_lv3")

class Tindakan(Base):
    __tablename__ = "tindakan"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id"), nullable=True)
    kondisi_awal = Column(String)
    tindakan = Column(String, nullable=True)
    kondisi_pasca = Column(String, nullable=True)
    id_masalah = Column(Integer, ForeignKey("masalah.id"))
    id_kategori = Column(Integer, ForeignKey("kategori_tindakan.id"), nullable=True)
    id_sarana = Column(Integer, ForeignKey("sarana.id"), nullable=True)
    id_ruangan = Column(Integer, ForeignKey("ruangan.id"))
    foto = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    done_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    kategori_tindakan = relationship("KategoriTindakan", back_populates="tindakan")
    sarana = relationship("Sarana", back_populates="tindakan")
    ruangan = relationship("Ruangan", back_populates="tindakan")
    masalah = relationship("Masalah", back_populates="tindakan")
    # user = relationship("User", back_populates="tindakan")
