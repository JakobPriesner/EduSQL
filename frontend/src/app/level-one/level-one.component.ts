import {Component, OnInit} from '@angular/core';
import {CookieService} from "../../lib/services/cookie.service";
import {ValidationService} from "../../lib/services/api/validation.service";
import {AbstractControl} from '@angular/forms';
import {STEPPER_GLOBAL_OPTIONS} from "@angular/cdk/stepper";
import {MatStepper} from "@angular/material/stepper";
import {LocalDbUserValidator} from "../../lib/validator/local-db-user.validator";
import {UserDataStore} from "../../lib/stores/user-data.store";

@Component({
  selector: 'app-level-one',
  templateUrl: './level-one.component.html',
  styleUrls: ['./level-one.component.scss'],
  providers: [
    {
      provide: STEPPER_GLOBAL_OPTIONS,
      useValue: {showError: true},
    },
  ]
})
export class LevelOneComponent implements OnInit{
  errorMessage: string = "";
  highestValidatedLevel: string = this.cookieService.getCookie("uuid")!;

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
    this.validationService.validateTask(1, task).subscribe(result => {
      if (result.isValid && this.highestValidatedLevel.localeCompare(result.level)) {
        this.highestValidatedLevel =  result.level;
      }
      if (result.isValid) {
        this.errorMessage = "";
        stepper.next();
      }
    });
  }

  validateDbUserLoginTask(stepper: MatStepper) {
    let validationResult = this.localDbUserValidator.validateLoggedInAsUser(1, 3, 's_krause');
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
