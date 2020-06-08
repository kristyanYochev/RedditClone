import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private accessToken: string;
  private refreshToken: string;

  private baseURL = 'http://127.0.0.1:3000';
  constructor(private http: HttpClient) { }

  registerUser(username: string, password: string) {
    return this.http.post(`${this.baseURL}/auth`, {
      username, password
    });
  }
}
