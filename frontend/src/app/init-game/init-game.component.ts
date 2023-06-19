import { Component } from '@angular/core';
import {UsersService} from "../../lib/services/api/users.service";
import {CookieService} from "../../lib/services/cookie.service";
import {MatSnackBar} from "@angular/material/snack-bar";
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {UserDataStore} from "../../lib/stores/user-data.store";
import {first} from "rxjs";

@Component({
  selector: 'app-init-game',
  templateUrl: './init-game.component.html',
  styleUrls: ['./init-game.component.css']
})
export class InitGameComponent {
  public isLoading: boolean = false;
  public newGameForm: FormGroup;
  public existingGameForm: FormGroup;
  public showError: boolean = false;

  constructor(private userService: UsersService,
              private cookieService: CookieService,
              private snackBar: MatSnackBar,
              private formBuilder: FormBuilder,
              private userDataStore: UserDataStore) {
    this.newGameForm = this.formBuilder.group({
      firstName: ["", Validators.required],
      lastName: ["", Validators.required],

    });

    this.existingGameForm = this.formBuilder.group({
      uuid: ["", Validators.required]
    })
  }

  submit() : void {
    if (!this.existingGameForm.valid && !this.newGameForm.valid) {
      this.showError = true;
      return;
    }
    this.isLoading = true;
    if (this.existingGameForm.valid) {
      this.verifyUser(this.existingGameForm.get('uuid')?.value);
    } else {
      this.registerUser();
    }
  }

  verifyUser(uuidInput: string) : void {
    this.userService.checkIfUserExists(uuidInput).subscribe(result => {
      if (result.exists) {
        this.cookieService.createCookie("uuid", uuidInput, 365);
      } else {
        this.snackBar.open("No project found with the UUID \"" + uuidInput + " \"! Try again or start a new game.")
      }
      this.isLoading = false;
    });
  }

  registerUser() : void {
    let firstName = this.newGameForm.get('firstName')!.value;
    let lastName = this.newGameForm.get('lastName')!.value
    this.userService.registerUser().subscribe(result => {
      this.cookieService.createCookie("uuid", result.userUuid, 7);
      this.userDataStore.firstName = firstName;
      this.userDataStore.lastName = lastName;
      this.isLoading = false;
    });
  }
}
