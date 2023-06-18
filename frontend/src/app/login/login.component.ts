import {Component, EventEmitter, Output} from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import {DbUserStore} from "../../lib/stores/db-user.store";
import {UsersService} from "../../lib/services/api/users.service";


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  invalidLoginData: boolean = false;

  @Output() onSuccessfulLogin: EventEmitter<any> = new EventEmitter<any>();

  usernameFormControl = new FormControl('', [
    Validators.required,
  ]);

  passwordFormControl = new FormControl('', [
    Validators.required,
  ]);

  constructor(private dbUserStore: DbUserStore,
              private usersService: UsersService) {
  }

  onLogin() : void {
    let username = this.usernameFormControl.getRawValue()!;
    let password = this.passwordFormControl.getRawValue()!;
    this.usersService.checkIfDbUserExists({username: username, password: password}).subscribe(result => {
      if (result.exists) {
        this.dbUserStore.username = username;
        this.dbUserStore.password = password;
        this.onSuccessfulLogin.emit();
      } else {
        this.invalidLoginData = true;
      }
    })
  }
}
