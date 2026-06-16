-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 16 Jun 2026 pada 11.08
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `konsumtif_db`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `dataset_pengguna`
--

CREATE TABLE `dataset_pengguna` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `x01` int(11) NOT NULL,
  `x02` int(11) NOT NULL,
  `x03` int(11) NOT NULL,
  `x04` int(11) NOT NULL,
  `x05` int(11) NOT NULL,
  `x06` int(11) NOT NULL,
  `x07` int(11) NOT NULL,
  `x08` int(11) NOT NULL,
  `x09` int(11) NOT NULL,
  `x10` int(11) NOT NULL,
  `x11` int(11) NOT NULL,
  `x12` int(11) NOT NULL,
  `x13` int(11) NOT NULL,
  `x14` int(11) NOT NULL,
  `x15` int(11) NOT NULL,
  `x16` int(11) NOT NULL,
  `x17` int(11) NOT NULL,
  `x18` int(11) NOT NULL,
  `x19` int(11) NOT NULL,
  `x20` int(11) NOT NULL,
  `x21` int(11) NOT NULL,
  `x22` int(11) NOT NULL,
  `x23` int(11) NOT NULL,
  `x24` int(11) NOT NULL,
  `x25` int(11) NOT NULL,
  `x26` int(11) NOT NULL,
  `x27` int(11) NOT NULL,
  `x28` int(11) NOT NULL,
  `intensitas_ewallet` varchar(20) DEFAULT NULL,
  `aktivitas_ewallet` varchar(20) DEFAULT NULL,
  `intensitas_paylater` varchar(20) DEFAULT NULL,
  `dampak_paylater` varchar(20) DEFAULT NULL,
  `pengaruh_promo` varchar(20) DEFAULT NULL,
  `sosial_lingkungan` varchar(20) DEFAULT NULL,
  `media_gayahidup` varchar(20) DEFAULT NULL,
  `kontrol_pengeluaran` varchar(20) DEFAULT NULL,
  `kontrol_literasi` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `tanggal_input` timestamp NOT NULL DEFAULT current_timestamp(),
  `jk` varchar(20) DEFAULT NULL,
  `usia` varchar(50) DEFAULT NULL,
  `pekerjaan` varchar(100) DEFAULT NULL,
  `pendapatan` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `dataset_training`
--

CREATE TABLE `dataset_training` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `intensitas_ewallet` varchar(20) DEFAULT NULL,
  `aktivitas_ewallet` varchar(20) DEFAULT NULL,
  `intensitas_paylater` varchar(20) DEFAULT NULL,
  `dampak_paylater` varchar(20) DEFAULT NULL,
  `pengaruh_promo` varchar(20) DEFAULT NULL,
  `sosial_lingkungan` varchar(20) DEFAULT NULL,
  `media_gayahidup` varchar(20) DEFAULT NULL,
  `kontrol_pengeluaran` varchar(20) DEFAULT NULL,
  `kontrol_literasi` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `admin_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `hasil_prediksi`
--

CREATE TABLE `hasil_prediksi` (
  `id` int(11) NOT NULL,
  `hasil` varchar(20) DEFAULT NULL,
  `rekomendasi` text DEFAULT NULL,
  `insight` text DEFAULT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `dataset_pengguna_id` int(11) DEFAULT NULL,
  `dataset_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','user') DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `dataset_pengguna`
--
ALTER TABLE `dataset_pengguna`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeks untuk tabel `dataset_training`
--
ALTER TABLE `dataset_training`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_training_user` (`admin_id`);

--
-- Indeks untuk tabel `hasil_prediksi`
--
ALTER TABLE `hasil_prediksi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `idx_dataset_pengguna` (`dataset_pengguna_id`),
  ADD KEY `idx_dataset_id` (`dataset_id`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `dataset_pengguna`
--
ALTER TABLE `dataset_pengguna`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `dataset_training`
--
ALTER TABLE `dataset_training`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `hasil_prediksi`
--
ALTER TABLE `hasil_prediksi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `dataset_pengguna`
--
ALTER TABLE `dataset_pengguna`
  ADD CONSTRAINT `fk_dataset_pengguna_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `dataset_training`
--
ALTER TABLE `dataset_training`
  ADD CONSTRAINT `fk_training_user` FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `hasil_prediksi`
--
ALTER TABLE `hasil_prediksi`
  ADD CONSTRAINT `fk_hasil_dataset` FOREIGN KEY (`dataset_pengguna_id`) REFERENCES `dataset_pengguna` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_hasil_prediksi_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
