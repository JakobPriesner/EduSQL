import { Component } from '@angular/core';
import {CookieService} from "../../lib/services/cookie.service";
import {ValidationService} from "../../lib/services/api/validation.service";
import {STEPPER_GLOBAL_OPTIONS} from "@angular/cdk/stepper";
import {MatStepper} from "@angular/material/stepper";
import {LocalDbUserValidator} from "../../lib/validator/local-db-user.validator";
import {UserDataStore} from "../../lib/stores/user-data.store";
import {MatSlideToggleChange} from "@angular/material/slide-toggle";
import {SqlService} from "../../lib/services/api/sql.service";
import {SqlResult} from "../../lib/models/sqlResult";

@Component({
  selector: 'app-level-twelve',
  templateUrl: './level-twelve.component.html',
  styleUrls: ['./level-twelve.component.scss'],
  providers: [
    {
      provide: STEPPER_GLOBAL_OPTIONS,
      useValue: {showError: true},
    },
  ]
})
export class LevelTwelveComponent {


  errorMessage: string = "";
  highestValidatedLevel: string = "0.0";

  useDefault: boolean = false;
  toggle(event: MatSlideToggleChange) {
    console.log('toggle', event.checked);
    this.useDefault = event.checked;
  }

  constructor(private cookieService: CookieService,
              private validationService: ValidationService,
              public localDbUserValidator: LocalDbUserValidator,
              public userDataStore: UserDataStore,
              private sqlService: SqlService) {

  }

  // @ts-ignore
  sqlResult: SqlResult = [];

  ngOnInit() {
    this.sqlService.executeSql("SELECT * FROM location WHERE id = 2;").subscribe(result => {
      this.sqlResult = result;
    });

  }


  deleteSqlExecute(to: string, stepper: MatStepper) : void {
    let payload: { [key: string]: any } = {
      answer: this.useDefault
    };
    this.validationService.validateTaskWithPayload(12, 2, payload).subscribe(result => {
      console.log(result)
      if(result.isValid)
      {
        if (this.highestValidatedLevel.localeCompare(to)) {
          this.highestValidatedLevel =  to;
        }
        this.errorMessage = "";
        stepper.next();
      }
    });
  }

  onSuccessfulLogin(stepper: MatStepper) : void {
    this.errorMessage="";
    stepper.next();
  }

  validateDbUserLoginTask(stepper: MatStepper) {
    let validationResult = this.localDbUserValidator.validateLoggedInAsUser(12, 1, 'm_rott');
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

