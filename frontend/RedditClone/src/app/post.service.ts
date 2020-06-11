import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class PostService {
  private baseURL = 'http://127.0.0.1:3000';
  constructor(private http: HttpClient, private auth: AuthService) { }

  addPost(title: string, content: string, subredditName: string) {
    console.log(this.auth.getAccessToken());
    return this.http.post(`${this.baseURL}/posts`, {
      title, content, subredditName
    }, {headers: {Authorization: `Bearer ${this.auth.getAccessToken()}`}});
  }

  editPost(title: string, content: string) {
    return this.http.put(`${this.baseURL}/posts`, {
      title, content
    });
  }
}
