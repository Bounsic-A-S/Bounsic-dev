import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment.dev';

@Injectable({
  providedIn: 'root'
})
export class HealthService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}
  getHealth(): Observable<any> {
    return this.http.get(`${this.apiUrl}/health`);
  }
}
