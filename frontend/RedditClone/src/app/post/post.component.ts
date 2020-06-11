import { Component, OnInit } from '@angular/core';
import { PostService } from '../post.service';

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.scss']
})
export class PostComponent implements OnInit {
  title: string;
  content: string;
  subredditName: string;
  error: string;

  constructor(private post: PostService) { }

  ngOnInit() {
  }

  addPost() {
    this.post.addPost(this.title, this.content, this.subredditName).subscribe(console.log);
  }

}
