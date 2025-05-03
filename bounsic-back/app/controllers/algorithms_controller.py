from fastapi import HTTPException
# from app.services.algorithms_service import generate_fingerprint
from app.services.algorithms.fingerprint_service import generate_fingerprint

class Algoritms_controller:
    
    @staticmethod
    def fingerprint(songName: str):
        # if not song?:
        #     raise HTTPException(status_code=400, detail="Song not found")
        res = generate_fingerprint(songName=songName)
        
        if not res:
            raise HTTPException(status_code=404, detail="No se encontraron datos")

        return {"data": res}
