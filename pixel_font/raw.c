
#include "lvgl/lvgl.h"

/***********************************************************************************
 * 3-by-5-pixel-font.ttf 5 px Font in U+0020 ( ) .. U+007e (~)  range with 1 bpp
 * Sparse font with only these characters: ABCDEFGHIJKLMNOPQRSTUVWXYZ
***********************************************************************************/

/*Store the image of the letters (glyph)*/
static const uint8_t raw_glyph_bitmap[] = 
{
  /*Unicode: U+0041 (A) , Width: 3 */
  0xe0,  //%%% 
  0xa0,  //%.% 
  0xe0,  //%%% 
  0xa0,  //%.% 
  0xa0,  //%.% 


  /*Unicode: U+0042 (B) , Width: 3 */
  0xc0,  //%%. 
  0xa0,  //%.% 
  0xc0,  //%%. 
  0xa0,  //%.% 
  0xc0,  //%%. 


  /*Unicode: U+0043 (C) , Width: 3 */
  0x60,  //.%% 
  0x80,  //%.. 
  0x80,  //%.. 
  0x80,  //%.. 
  0x60,  //.%% 


  /*Unicode: U+0044 (D) , Width: 3 */
  0xc0,  //%%. 
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xc0,  //%%. 


  /*Unicode: U+0045 (E) , Width: 3 */
  0xe0,  //%%% 
  0x80,  //%.. 
  0xe0,  //%%% 
  0x80,  //%.. 
  0xe0,  //%%% 


  /*Unicode: U+0046 (F) , Width: 3 */
  0xe0,  //%%% 
  0x80,  //%.. 
  0xe0,  //%%% 
  0x80,  //%.. 
  0x80,  //%.. 


  /*Unicode: U+0047 (G) , Width: 3 */
  0x60,  //.%% 
  0x80,  //%.. 
  0xa0,  //%.% 
  0xa0,  //%.% 
  0x60,  //.%% 


  /*Unicode: U+0048 (H) , Width: 3 */
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xe0,  //%%% 
  0xa0,  //%.% 
  0xa0,  //%.% 


  /*Unicode: U+0049 (I) , Width: 3 */
  0xe0,  //%%% 
  0x40,  //.%. 
  0x40,  //.%. 
  0x40,  //.%. 
  0xe0,  //%%% 


  /*Unicode: U+004a (J) , Width: 3 */
  0x20,  //..% 
  0x20,  //..% 
  0x20,  //..% 
  0xa0,  //%.% 
  0xe0,  //%%% 


  /*Unicode: U+004b (K) , Width: 3 */
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xc0,  //%%. 
  0xa0,  //%.% 
  0xa0,  //%.% 


  /*Unicode: U+004c (L) , Width: 3 */
  0x80,  //%.. 
  0x80,  //%.. 
  0x80,  //%.. 
  0x80,  //%.. 
  0xe0,  //%%% 


  /*Unicode: U+004d (M) , Width: 3 */
  0xa0,  //%.% 
  0xe0,  //%%% 
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xa0,  //%.% 


  /*Unicode: U+004e (N) , Width: 3 */
  0xe0,  //%%% 
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xa0,  //%.% 


  /*Unicode: U+004f (O) , Width: 3 */
  0xe0,  //%%% 
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xe0,  //%%% 


  /*Unicode: U+0050 (P) , Width: 3 */
  0xe0,  //%%% 
  0xa0,  //%.% 
  0xe0,  //%%% 
  0x80,  //%.. 
  0x80,  //%.. 


  /*Unicode: U+0051 (Q) , Width: 3 */
  0xc0,  //%%% 
  0xc0,  //%.% 
  0xc0,  //%.% 
  0xc0,  //%%% 
  0xe0,  //..% 


  /*Unicode: U+0052 (R) , Width: 3 */
  0xc0,  //%%. 
  0xa0,  //%.% 
  0xc0,  //%%. 
  0xa0,  //%.% 
  0xa0,  //%.% 


  /*Unicode: U+0053 (S) , Width: 3 */
  0x60,  //.%% 
  0x80,  //%.. 
  0x40,  //.%. 
  0x20,  //..% 
  0xc0,  //%%. 


  /*Unicode: U+0054 (T) , Width: 3 */
  0xe0,  //%%% 
  0x40,  //.%. 
  0x40,  //.%. 
  0x40,  //.%. 
  0x40,  //.%. 


  /*Unicode: U+0055 (U) , Width: 3 */
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xe0,  //%%% 


  /*Unicode: U+0056 (V) , Width: 3 */
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xc0,  //.%. 


  /*Unicode: U+0057 (W) , Width: 3 */
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xe0,  //%%% 
  0xa0,  //%.% 


  /*Unicode: U+0058 (X) , Width: 3 */
  0xa0,  //%.% 
  0xa0,  //%.% 
  0x40,  //.%. 
  0xa0,  //%.% 
  0xa0,  //%.% 


  /*Unicode: U+0059 (Y) , Width: 3 */
  0xa0,  //%.% 
  0xa0,  //%.% 
  0xe0,  //%%% 
  0x40,  //.%. 
  0x40,  //.%. 


  /*Unicode: U+005a (Z) , Width: 3 */
  0xe0,  //%%% 
  0x20,  //..% 
  0x40,  //.%. 
  0x80,  //%.. 
  0xe0,  //%%% 


};


/*Store the glyph descriptions*/
static const lv_font_glyph_dsc_t raw_glyph_dsc[] = 
{
  {.w_px = 3,	.glyph_index = 0},	/*Unicode: U+0041 (A)*/
  {.w_px = 3,	.glyph_index = 5},	/*Unicode: U+0042 (B)*/
  {.w_px = 3,	.glyph_index = 10},	/*Unicode: U+0043 (C)*/
  {.w_px = 3,	.glyph_index = 15},	/*Unicode: U+0044 (D)*/
  {.w_px = 3,	.glyph_index = 20},	/*Unicode: U+0045 (E)*/
  {.w_px = 3,	.glyph_index = 25},	/*Unicode: U+0046 (F)*/
  {.w_px = 3,	.glyph_index = 30},	/*Unicode: U+0047 (G)*/
  {.w_px = 3,	.glyph_index = 35},	/*Unicode: U+0048 (H)*/
  {.w_px = 3,	.glyph_index = 40},	/*Unicode: U+0049 (I)*/
  {.w_px = 3,	.glyph_index = 45},	/*Unicode: U+004a (J)*/
  {.w_px = 3,	.glyph_index = 50},	/*Unicode: U+004b (K)*/
  {.w_px = 3,	.glyph_index = 55},	/*Unicode: U+004c (L)*/
  {.w_px = 3,	.glyph_index = 60},	/*Unicode: U+004d (M)*/
  {.w_px = 3,	.glyph_index = 65},	/*Unicode: U+004e (N)*/
  {.w_px = 3,	.glyph_index = 70},	/*Unicode: U+004f (O)*/
  {.w_px = 3,	.glyph_index = 75},	/*Unicode: U+0050 (P)*/
  {.w_px = 3,	.glyph_index = 80},	/*Unicode: U+0051 (Q)*/
  {.w_px = 3,	.glyph_index = 85},	/*Unicode: U+0052 (R)*/
  {.w_px = 3,	.glyph_index = 90},	/*Unicode: U+0053 (S)*/
  {.w_px = 3,	.glyph_index = 95},	/*Unicode: U+0054 (T)*/
  {.w_px = 3,	.glyph_index = 100},	/*Unicode: U+0055 (U)*/
  {.w_px = 3,	.glyph_index = 105},	/*Unicode: U+0056 (V)*/
  {.w_px = 3,	.glyph_index = 110},	/*Unicode: U+0057 (W)*/
  {.w_px = 3,	.glyph_index = 115},	/*Unicode: U+0058 (X)*/
  {.w_px = 3,	.glyph_index = 120},	/*Unicode: U+0059 (Y)*/
  {.w_px = 3,	.glyph_index = 125},	/*Unicode: U+005a (Z)*/
};

/*List of unicode characters*/
static const uint32_t raw_unicode_list[] = {
  65,	/*Unicode: U+0041 (A)*/
  66,	/*Unicode: U+0042 (B)*/
  67,	/*Unicode: U+0043 (C)*/
  68,	/*Unicode: U+0044 (D)*/
  69,	/*Unicode: U+0045 (E)*/
  70,	/*Unicode: U+0046 (F)*/
  71,	/*Unicode: U+0047 (G)*/
  72,	/*Unicode: U+0048 (H)*/
  73,	/*Unicode: U+0049 (I)*/
  74,	/*Unicode: U+004a (J)*/
  75,	/*Unicode: U+004b (K)*/
  76,	/*Unicode: U+004c (L)*/
  77,	/*Unicode: U+004d (M)*/
  78,	/*Unicode: U+004e (N)*/
  79,	/*Unicode: U+004f (O)*/
  80,	/*Unicode: U+0050 (P)*/
  81,	/*Unicode: U+0051 (Q)*/
  82,	/*Unicode: U+0052 (R)*/
  83,	/*Unicode: U+0053 (S)*/
  84,	/*Unicode: U+0054 (T)*/
  85,	/*Unicode: U+0055 (U)*/
  86,	/*Unicode: U+0056 (V)*/
  87,	/*Unicode: U+0057 (W)*/
  88,	/*Unicode: U+0058 (X)*/
  89,	/*Unicode: U+0059 (Y)*/
  90,	/*Unicode: U+005a (Z)*/
  0,    /*End indicator*/
};

lv_font_t raw = 
{
    .unicode_first = 32,	/*First Unicode letter in this font*/
    .unicode_last = 126,	/*Last Unicode letter in this font*/
    .h_px = 5,				/*Font height in pixels*/
    .glyph_bitmap = raw_glyph_bitmap,	/*Bitmap of glyphs*/
    .glyph_dsc = raw_glyph_dsc,		/*Description of glyphs*/
    .glyph_cnt = 26,			/*Number of glyphs in the font*/
    .unicode_list = raw_unicode_list,	/*List of unicode characters*/
    .get_bitmap = lv_font_get_bitmap_sparse,	/*Function pointer to get glyph's bitmap*/
    .get_width = lv_font_get_width_sparse,	/*Function pointer to get glyph's width*/
    .bpp = 1,				/*Bit per pixel*/
    .monospace = 3,		/*Fix width (0: if not used)*/
    .next_page = NULL,		/*Pointer to a font extension*/
};
