import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class PostService {
  private baseURL = 'http://127.0.0.1:3000';
  constructor(private http: HttpClient) { }

  addPost(title: string, content: string, subredditName: string) {
    return this.http.post(`${this.baseURL}/posts`, {
      title, content, subredditName
    });
  }

  editPost(title: string, content: string) {
    return this.http.put(`${this.baseURL}/posts`, {
      title, content
    });
  }
}
