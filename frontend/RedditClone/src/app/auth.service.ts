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

  logInUser(username: string, password: string) {
    const request =  this.http.put(`${this.baseURL}/auth`, {
      username, password
    });
    request.subscribe((resp: any) => {
      this.accessToken = resp.access_token;
      this.refreshToken = resp.refresh_token;
    }, (error) => {
      console.log(error);
    });
    return request;
  }

  getAccessToken() {
    return this.accessToken;
  }
}
