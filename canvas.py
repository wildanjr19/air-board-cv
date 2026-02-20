"""
Virtual canvas untuk menggambar dengan mendeteksi gestur tangan. 
Canvas ini transparan dan dapat digambar dengan garis atau titik.
"""
import cv2
import numpy as np
from typing import Tuple, Optional


class DrawingCanvas:
    """Transparent canvas for drawing with hand gestures"""
    
    def __init__(self, width: int = 640, height: int = 480):
        """
        Inisialisasi canvas
        
        Args:
            width: lebar canvas
            height: tinggi canvas
        """
        self.width = width
        self.height = height
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.prev_point = None
        self.brush_size = 5 # ukuran kuas untuk menggambar
        self.eraser_size = 30 # ukuran area yang dihapus
        
    def reset(self):
        """Hapus isi canvas"""
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.prev_point = None
    
    def draw_line(self, start: Tuple[int, int], end: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        """
        Gambar garis pada canvas.
        Pakai .line dari cv2 untuk menggambar garis antara start dan end dengan warna tertentu.
        
        Args:
            start: Starting point (x, y)
            end: Ending point (x, y)
            color: BGR color tuple
        """
        if start is None or end is None:
            return
            
        cv2.line(self.canvas, start, end, color, self.brush_size)
    
    def draw_point(self, point: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        """
        Gambar titik atau point di canvas.
        Pakai .circle dari cv2 untuk menggambar titik dengan radius sesuai brush_size.
        
        Args:
            point: koordinat titik (x, y)
            color: BGR color tuple
        """
        if point is None:
            return
            
        cv2.circle(self.canvas, point, self.brush_size, color, -1)
    
    def draw_from_previous(self, current_point: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        """
        Draw dari sebelumnya (titik atau line) ke titik saat ini.
        
        Args:
            current_point: titik saat ini
            color: BGR color tuple
        """
        if current_point is None:
            return
            
        if self.prev_point is not None:
            self.draw_line(self.prev_point, current_point, color)
        else:
            self.draw_point(current_point, color)
            
        self.prev_point = current_point
    
    def clear_previous(self) -> None:
        """Clear the previous point (call when finger lifted)"""
        self.prev_point = None
    
    def erase_at(self, point: Tuple[int, int]) -> None:
        """
        hapus gambar di area
        
        Args:
            point: titik tengah area yang dihapus (x, y)
        """
        if point is None:
            return
            
        x, y = point
        # buat pengghapus bentuk circle
        cv2.circle(self.canvas, (x, y), self.eraser_size, (0, 0, 0), -1)
    
    def get_canvas(self) -> np.ndarray:
        """kembalikan canvas saat ini"""
        return self.canvas
    
    def resize(self, width: int, height: int) -> None:
        """
        resize ukuran canvas
        
        Args:
            width: New width
            height: New height
        """
        self.width = width
        self.height = height
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.prev_point = None
    
    def add_to_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        overlay canvas ke frame video. pakai alpha blending untuk menggabungkan canvas dengan frame asli.
        
        Args:
            frame: frame video asli dari webcam
            
        Returns:
            video frame dengan canvas digabungkan
        """
        # Use alpha blending for smooth overlay
        # Create a mask where we have drawn
        mask = np.any(self.canvas > 0, axis=2)
        
        # Where we have drawing, use the drawing; otherwise use frame
        result = frame.copy()
        result[mask] = self.canvas[mask]
        
        return result
