import unittest
from unittest.mock import patch, MagicMock
import requests
from app.services.srapping_service import get_lyrics

class TestGetLyrics(unittest.TestCase):
    
    @patch('requests.get')
    def test_successful_lyrics_retrieval(self):
        expect = """Estrellita, ¿dónde estás?
        Me pregunto quién serás
        En el cielo o en el mar
        Un diamante de verdad

        Estrellita, ¿dónde estás?
        Me pregunto quién serás

        En el cielo o en el mar
        Un diamante de verdad
        Estrellita, ¿dónde estás?
        Me pregunto quién serás

        Estrellita, ¿dónde estás?
        Me pregunto quién serás
        En el cielo o en el mar
        Un diamante de verdad

        Estrellita, ¿dónde estás?
        Me pregunto quién serás"""
        self.assertEqual(get_lyrics("estrellita donde estas", "canciones para nios"))


    # @patch('requests.get')
    # def test_lyrics_not_found(self, mock_get):
    #     """Test cuando no se encuentra el div de letras"""
    #     mock_response = MagicMock()
    #     mock_response.status_code = 200
    #     mock_response.text = '<html><body>No hay letras aquí</body></html>'
    #     mock_get.return_value = mock_response
        
    #     result = get_lyrics("no lyrics", "test artist")
    #     self.assertEqual(result, "Letra no encontrada")
    

    # @patch('requests.get')
    # def test_connection_error(self, mock_get):
    #     """Test cuando hay error de conexión"""
    #     mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
    #     result = get_lyrics("test", "song")
    #     self.assertIn("Connection failed", result)
    


if __name__ == '__main__':
    unittest.main()