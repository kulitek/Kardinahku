from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
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
    id_pegawai = Column(Integer, ForeignKey("pegawai.id"))

    created_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)

    pegawai = relationship("Pegawai", back_populates="user")


class Pegawai(Base):
    __tablename__ = "pegawai"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150))
    nama_lengkap = Column(String(60))
    nama_panggilan = Column(String(60), nullable=True)
    tempat_lahir = Column(String(20), nullable=True)
    tanggal_lahir = Column(DateTime, nullable=True)
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

class Ruangan(Base):
    __tablename__ = "ruangan"

    id = Column(Integer, primary_key=True, index=True)


class Masalah(Base):
    __tablename__ = "masalah"

    id = Column(Integer, primary_key=True, index=True)
    deskripsi = Column(Text)
    id_kategori_masalah = Column(Integer, ForeignKey("kategori_masalah.id"))
    id_ruangan = Column(Integer, ForeignKey("ruangan.id"))
