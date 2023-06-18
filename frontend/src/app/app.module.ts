import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { InitGameComponent } from './init-game/init-game.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {RouterOutlet} from "@angular/router";
import {MatToolbarModule} from "@angular/material/toolbar";
import {MatIconModule} from "@angular/material/icon";
import {MatButtonModule} from "@angular/material/button";
import {MatInputModule} from "@angular/material/input";
import {HttpClientModule} from "@angular/common/http";
import {MatSnackBarModule} from "@angular/material/snack-bar";
import {CommonModule} from "@angular/common";
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";
import {MatProgressBarModule} from "@angular/material/progress-bar";
import { GameComponent } from './game/game.component';
import {MatStepperModule} from "@angular/material/stepper";
import { LevelOneComponent } from './level-one/level-one.component';
import { ErmDialogComponent } from './erm-dialog/erm-dialog.component';
import {MatDialogModule} from "@angular/material/dialog";
import {NgxImageZoomModule} from "ngx-image-zoom";
import { AlertComponent } from './alert/alert.component';
import {ReactiveFormsModule} from "@angular/forms";
import {MatFormFieldModule} from "@angular/material/form-field";
import { LoginComponent } from './login/login.component';
import {MatCardModule} from "@angular/material/card";
import { LevelTwoComponent } from './level-two/level-two.component';

@NgModule({
    declarations: [
        AppComponent,
        InitGameComponent,
        GameComponent,
        LevelOneComponent,
        ErmDialogComponent,
        AlertComponent,
        LoginComponent,
        LevelTwoComponent
    ],
  imports: [
    HttpClientModule,
    BrowserModule,
    BrowserAnimationsModule,
    CommonModule,
    RouterOutlet,
    MatToolbarModule,
    MatIconModule,
    MatButtonModule,
    MatInputModule,
    MatSnackBarModule,
    MatProgressSpinnerModule,
    MatProgressBarModule,
    MatStepperModule,
    MatDialogModule,
    NgxImageZoomModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatCardModule,
  ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
