import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment.dev';

@Injectable({
  providedIn: 'root'
})
export class AudioStreamService {
    private baseUrl = environment.api_S_Url;
  
    getAudioUrl(blobName: string): string {
      return `${this.baseUrl}/stream/${encodeURIComponent(blobName)}`;
    }
  }
