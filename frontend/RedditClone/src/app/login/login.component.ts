import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
 
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  username: string;
  password: string;
  error: string;

  constructor(private auth: AuthService, private router: Router) { }

  ngOnInit() {
  }

  logIn() {
    this.auth.logInUser(this.username, this.password);
  }

  redirectToPost() {
    this.router.navigateByUrl('/post');
  }
}
