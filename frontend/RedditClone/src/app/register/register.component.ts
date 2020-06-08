import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {
  username: string;
  password: string;
  repeatPassword: string;

  constructor(private auth: AuthService) { }

  ngOnInit() {
  }

  registerUser() {
    if (this.password !== this.repeatPassword) {
      alert('Passwords do not match');
      return;
    }

    this.auth.registerUser(this.username, this.password).subscribe(console.log);
  }
}
