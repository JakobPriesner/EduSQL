import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import { FileSaverService } from 'ngx-filesaver';
import {MatDialogRef} from "@angular/material/dialog";

@Component({
  selector: 'app-erm-dialog',
  templateUrl: './erm-dialog.component.html',
  styleUrls: ['./erm-dialog.component.scss']
})
export class ErmDialogComponent {
  zoom = 1;
  @ViewChild('zoomImage', { static: false }) imageContainer!: ElementRef;
  @ViewChild("ermImage") ermImage!: ElementRef;

  constructor(private _fileSaverService: FileSaverService,
              public dialogRef: MatDialogRef<ErmDialogComponent>) {

  }

  toggleFullScreen(element: HTMLElement) {
    if (!document.fullscreenElement) {
      element.requestFullscreen().catch(console.error);
    } else if (document.exitFullscreen) {
      document.exitFullscreen();
    }
  }

  zoomIn() {
    this.zoom *= 1.1;
    this.applyZoom();
  }

  zoomOut() {
    this.zoom *= 0.9;
    this.applyZoom();
  }

  private applyZoom() {
    this.ermImage.nativeElement.style.transform = `scale(${this.zoom})`;
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  downloadImage() {
    // Url of the image
    const imageUrl = 'assets/erm.png';

    // Fetch the image
    fetch(imageUrl)
        .then(response => response.blob())
        .then(blob => {
          // Use FileSaver to save the image
          this._fileSaverService.save(blob, 'erm.png');
        })
        .catch(err => console.error(err));
  }

  getMaxWidth() : number {
    return 300;
  }

  getMaxHeight() : number {
    return 400;
  }

}
