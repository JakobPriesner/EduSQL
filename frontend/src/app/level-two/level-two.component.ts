import { Component } from '@angular/core';
import {CookieService} from "../../lib/services/cookie.service";
import {ValidationService} from "../../lib/services/api/validation.service";
import {LocalDbUserValidator} from "../../lib/validator/local-db-user.validator";
import {UserDataStore} from "../../lib/stores/user-data.store";
import {AbstractControl} from "@angular/forms";
import {MatStepper} from "@angular/material/stepper";

@Component({
  selector: 'app-level-two',
  templateUrl: './level-two.component.html',
  styleUrls: ['./level-two.component.css']
})
export class LevelTwoComponent {
  errorMessage: string = "";
  highestValidatedLevel: string = "0.0";

  constructor(private cookieService: CookieService,
              private validationService: ValidationService,
              public localDbUserValidator: LocalDbUserValidator,
              public userDataStore: UserDataStore) {

  }

  ngOnInit() {

  }

  cookieValidator(control: AbstractControl): { [key: string]: any } | null {
    const formValue = control.value;
    const cookieValue = this.cookieService.getCookie('cookieName');
    if (cookieValue == null) {
      return { 'cookieExists': false };
    }
    return cookieValue.localeCompare(formValue) >= 0 ? null : { 'stepValidated': false };
  }

  validateStep(task: number, stepper: MatStepper) : void {
    this.validationService.validateTask(2, task).subscribe(result => {
      if (result.isValid && this.highestValidatedLevel.localeCompare(result.level)) {
        this.highestValidatedLevel =  result.level;
      }
      if (result.isValid) {
        this.errorMessage = "";
        stepper.next();
      }
    });
  }

  validateDbUserLoginTask(stepper: MatStepper) { // todo: welcher stepper wird verwendt? Wie wird der Task gesetzt? mit .next im HTML?
    let validationResult = this.localDbUserValidator.validateLoggedInAsUser(2, 2, this.userDataStore.firstName); // todo: welcher Name?
    this.errorMessage = validationResult.message;
    if (validationResult.isValid) {
      this.updateHighestValidationStep(validationResult.level, stepper);
    }
  }

  updateHighestValidationStep(to: string, stepper: MatStepper) : void {
    if (this.highestValidatedLevel.localeCompare(to)) {
      this.highestValidatedLevel =  to;
    }
    this.errorMessage = "";
    stepper.next();
  }
}
