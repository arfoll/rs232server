#include "termkey.h"
#include "termkey-internal.h"

#include <stdio.h>
#include <string.h>

// There are 64 codes 0x40 - 0x7F
static int keyinfo_initialised = 0;
static struct keyinfo ss3s[64];
static char ss3_kpalts[64];

typedef struct {
  TermKey *tk;
} TermKeyCsi;

typedef TermKeyResult CsiHandler(TermKey *tk, TermKeyKey *key, int cmd, long *arg, int args);
static CsiHandler *csi_handlers[64];

/*
 * Handler for CSI/SS3 cmd keys
 */

static struct keyinfo csi_ss3s[64];

static TermKeyResult handle_csi_ss3_full(TermKey *tk, TermKeyKey *key, int cmd, long *arg, int args)
{
  if(args > 1 && arg[1] != -1)
    key->modifiers = arg[1] - 1;
  else
    key->modifiers = 0;

  key->type = csi_ss3s[cmd - 0x40].type;
  key->code.sym = csi_ss3s[cmd - 0x40].sym;
  key->modifiers &= ~(csi_ss3s[cmd - 0x40].modifier_mask);
  key->modifiers |= csi_ss3s[cmd - 0x40].modifier_set;

  if(key->code.sym == TERMKEY_SYM_UNKNOWN)
    return TERMKEY_RES_NONE;

  return TERMKEY_RES_KEY;
}

static void register_csi_ss3_full(TermKeyType type, TermKeySym sym, int modifier_set, int modifier_mask, unsigned char cmd)
{
  if(cmd < 0x40 || cmd >= 0x80) {
    return;
  }

  csi_ss3s[cmd - 0x40].type = type;
  csi_ss3s[cmd - 0x40].sym = sym;
  csi_ss3s[cmd - 0x40].modifier_set = modifier_set;
  csi_ss3s[cmd - 0x40].modifier_mask = modifier_mask;

  csi_handlers[cmd - 0x40] = &handle_csi_ss3_full;
}

static void register_csi_ss3(TermKeyType type, TermKeySym sym, unsigned char cmd)
{
  register_csi_ss3_full(type, sym, 0, 0, cmd);
}

/*
 * Handler for SS3 keys with kpad alternate representations
 */

static void register_ss3kpalt(TermKeyType type, TermKeySym sym, unsigned char cmd, char kpalt)
{
  if(cmd < 0x40 || cmd >= 0x80) {
    return;
  }

  ss3s[cmd - 0x40].type = type;
  ss3s[cmd - 0x40].sym = sym;
  ss3s[cmd - 0x40].modifier_set = 0;
  ss3s[cmd - 0x40].modifier_mask = 0;
  ss3_kpalts[cmd - 0x40] = kpalt;
}

/*
 * Handler for CSI number ~ function keys
 */

static struct keyinfo csifuncs[35]; /* This value must be increased if more CSI function keys are added */
#define NCSIFUNCS (sizeof(csifuncs)/sizeof(csifuncs[0]))

static TermKeyResult handle_csifunc(TermKey *tk, TermKeyKey *key, int cmd, long *arg, int args)
{
  if(args > 1 && arg[1] != -1)
    key->modifiers = arg[1] - 1;
  else
    key->modifiers = 0;

  key->type = TERMKEY_TYPE_KEYSYM;

  if(arg[0] == 27) {
    int mod = key->modifiers;
    (*tk->method.emit_codepoint)(tk, arg[2], key);
    key->modifiers |= mod;
  }
  else if(arg[0] >= 0 && arg[0] < NCSIFUNCS) {
    key->type = csifuncs[arg[0]].type;
    key->code.sym = csifuncs[arg[0]].sym;
    key->modifiers &= ~(csifuncs[arg[0]].modifier_mask);
    key->modifiers |= csifuncs[arg[0]].modifier_set;
  }
  else
    key->code.sym = TERMKEY_SYM_UNKNOWN;

  if(key->code.sym == TERMKEY_SYM_UNKNOWN) {
#ifdef DEBUG
    fprintf(stderr, "CSI: Unknown function key %ld\n", arg[0]);
#endif
    return TERMKEY_RES_NONE;
  }

  return TERMKEY_RES_KEY;
}

static void register_csifunc(TermKeyType type, TermKeySym sym, int number)
{
  if(number >= NCSIFUNCS) {
    return;
  }

  csifuncs[number].type = type;
  csifuncs[number].sym = sym;
  csifuncs[number].modifier_set = 0;
  csifuncs[number].modifier_mask = 0;

  csi_handlers['~' - 0x40] = &handle_csifunc;
}

/*
 * Handler for CSI u extended Unicode keys
 */

static TermKeyResult handle_csi_unicode(TermKey *tk, TermKeyKey *key, int cmd, long *arg, int args)
{
  if(args > 1 && arg[1] != -1)
    key->modifiers = arg[1] - 1;
  else
    key->modifiers = 0;

  int mod = key->modifiers;
  key->type = TERMKEY_TYPE_KEYSYM;
  (*tk->method.emit_codepoint)(tk, arg[0], key);
  key->modifiers |= mod;

  return TERMKEY_RES_KEY;
}

/*
 * Handler for CSI M / CSI m mouse events in SRG and rxvt encodings
 * Note: This does not handle X10 encoding
 */

static TermKeyResult handle_csi_mouse(TermKey *tk, TermKeyKey *key, int cmd, long *arg, int args)
{
  int initial = cmd >> 8;
  cmd &= 0xff;

  if(!initial && args >= 3) { // rxvt protocol
    key->type = TERMKEY_TYPE_MOUSE;
    key->code.mouse[0] = arg[0];

    key->modifiers     = (key->code.mouse[0] & 0x1c) >> 2;
    key->code.mouse[0] &= ~0x1c;

    termkey_key_set_linecol(key, arg[1], arg[2]);

    return TERMKEY_RES_KEY;
  }

  if(initial == '<' && args >= 3) { // SGR protocol
    key->type = TERMKEY_TYPE_MOUSE;
    key->code.mouse[0] = arg[0];

    key->modifiers     = (key->code.mouse[0] & 0x1c) >> 2;
    key->code.mouse[0] &= ~0x1c;

    termkey_key_set_linecol(key, arg[1], arg[2]);

    if(cmd == 'm') // release
      key->code.mouse[3] |= 0x80;

    return TERMKEY_RES_KEY;
  }

  return TERMKEY_RES_NONE;
}

/*
 * Handler for CSI R position reports
 */

static TermKeyResult handle_csi_position(TermKey *tk, TermKeyKey *key, int cmd, long *arg, int args)
{
  if(args < 2)
    return TERMKEY_RES_NONE;

  key->type = TERMKEY_TYPE_POSITION;
  termkey_key_set_linecol(key, arg[1], arg[0]);

  return TERMKEY_RES_KEY;
}

static int register_keys(void)
{
  int i;

  for(i = 0; i < 64; i++) {
    csi_ss3s[i].sym = TERMKEY_SYM_UNKNOWN;
    ss3s[i].sym     = TERMKEY_SYM_UNKNOWN;
    ss3_kpalts[i] = 0;
  }

  for(i = 0; i < NCSIFUNCS; i++)
    csifuncs[i].sym = TERMKEY_SYM_UNKNOWN;

  register_csi_ss3(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_UP,    'A');
  register_csi_ss3(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_DOWN,  'B');
  register_csi_ss3(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_RIGHT, 'C');
  register_csi_ss3(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_LEFT,  'D');
  register_csi_ss3(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_BEGIN, 'E');
  register_csi_ss3(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_END,   'F');
  register_csi_ss3(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_HOME,  'H');
  register_csi_ss3(TERMKEY_TYPE_FUNCTION, 1, 'P');
  register_csi_ss3(TERMKEY_TYPE_FUNCTION, 2, 'Q');
  register_csi_ss3(TERMKEY_TYPE_FUNCTION, 3, 'R');
  register_csi_ss3(TERMKEY_TYPE_FUNCTION, 4, 'S');

  register_csi_ss3_full(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_TAB, TERMKEY_KEYMOD_SHIFT, TERMKEY_KEYMOD_SHIFT, 'Z');

  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KPENTER,  'M', 0);
  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KPEQUALS, 'X', '=');
  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KPMULT,   'j', '*');
  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KPPLUS,   'k', '+');
  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KPCOMMA,  'l', ',');
  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KPMINUS,  'm', '-');
  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KPPERIOD, 'n', '.');
  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KPDIV,    'o', '/');
  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KP0,      'p', '0');
  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KP1,      'q', '1');
  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KP2,      'r', '2');
  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KP3,      's', '3');
  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KP4,      't', '4');
  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KP5,      'u', '5');
  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KP6,      'v', '6');
  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KP7,      'w', '7');
  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KP8,      'x', '8');
  register_ss3kpalt(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_KP9,      'y', '9');

  register_csifunc(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_FIND,      1);
  register_csifunc(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_INSERT,    2);
  register_csifunc(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_DELETE,    3);
  register_csifunc(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_SELECT,    4);
  register_csifunc(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_PAGEUP,    5);
  register_csifunc(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_PAGEDOWN,  6);
  register_csifunc(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_HOME,      7);
  register_csifunc(TERMKEY_TYPE_KEYSYM, TERMKEY_SYM_END,       8);

  register_csifunc(TERMKEY_TYPE_FUNCTION, 1,  11);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 2,  12);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 3,  13);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 4,  14);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 5,  15);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 6,  17);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 7,  18);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 8,  19);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 9,  20);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 10, 21);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 11, 23);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 12, 24);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 13, 25);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 14, 26);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 15, 28);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 16, 29);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 17, 31);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 18, 32);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 19, 33);
  register_csifunc(TERMKEY_TYPE_FUNCTION, 20, 34);

  csi_handlers['u' - 0x40] = &handle_csi_unicode;

  csi_handlers['M' - 0x40] = &handle_csi_mouse;
  csi_handlers['m' - 0x40] = &handle_csi_mouse;

  csi_handlers['R' - 0x40] = &handle_csi_position;

  keyinfo_initialised = 1;
  return 1;
}

static void *new_driver(TermKey *tk, const char *term)
{
  if(!keyinfo_initialised)
    if(!register_keys())
      return NULL;

  TermKeyCsi *csi = malloc(sizeof *csi);
  if(!csi)
    return NULL;

  csi->tk = tk;

  return csi;
}

static void free_driver(void *info)
{
  TermKeyCsi *csi = info;

  free(csi);
}

#define CHARAT(i) (tk->buffer[tk->buffstart + (i)])

static TermKeyResult peekkey_csi(TermKey *tk, TermKeyCsi *csi, size_t introlen, TermKeyKey *key, int force, size_t *nbytep)
{
  size_t csi_end = introlen;

  while(csi_end < tk->buffcount) {
    if(CHARAT(csi_end) >= 0x40 && CHARAT(csi_end) < 0x80)
      break;
    csi_end++;
  }

  if(csi_end >= tk->buffcount) {
    if(!force)
      return TERMKEY_RES_AGAIN;

    (*tk->method.emit_codepoint)(tk, '[', key);
    key->modifiers |= TERMKEY_KEYMOD_ALT;
    *nbytep = introlen;
    return TERMKEY_RES_KEY;
  }

  unsigned char cmd = CHARAT(csi_end);
  long arg[16];
  char present = 0;
  int args = 0;
  int initial = 0;

  size_t p = introlen;

  // See if there is an initial byte
  if(CHARAT(p) >= '<' && CHARAT(p) <= '?') {
    initial = CHARAT(p);
    p++;
  }

  // Now attempt to parse out up number;number;... separated values
  while(p < csi_end) {
    unsigned char c = CHARAT(p);

    if(c >= '0' && c <= '9') {
      if(!present) {
        arg[args] = c - '0';
        present = 1;
      }
      else {
        arg[args] = (arg[args] * 10) + c - '0';
      }
    }
    else if(c == ';') {
      if(!present)
        arg[args] = -1;
      present = 0;
      args++;

      if(args > 16)
        break;
    }

    p++;
  }

  if(!present)
    arg[args] = -1;

  args++;

  if(cmd == 'M' && args < 3) { // Mouse in X10 encoding consumes the next 3 bytes also
    size_t csi_len = csi_end + 1;

    tk->buffstart += csi_len;
    tk->buffcount -= csi_len;

    TermKeyResult mouse_result = (*tk->method.peekkey_mouse)(tk, key, nbytep);

    tk->buffstart -= csi_len;
    tk->buffcount += csi_len;

    if(mouse_result == TERMKEY_RES_KEY)
      *nbytep += csi_len;

    return mouse_result;
  }

  TermKeyResult result = TERMKEY_RES_NONE;

  // We know from the logic above that cmd must be >= 0x40 and < 0x80
  if(csi_handlers[cmd - 0x40])
    result = (*csi_handlers[cmd - 0x40])(tk, key, (initial<<8)|cmd, arg, args);

  if(key->code.sym == TERMKEY_SYM_UNKNOWN) {
#ifdef DEBUG
    switch(args) {
      case 1:
        fprintf(stderr, "CSI: Unknown arg1=%ld cmd=%c\n", arg[0], (char)cmd);
        break;
      case 2:
        fprintf(stderr, "CSI: Unknown arg1=%ld arg2=%ld cmd=%c\n", arg[0], arg[1], (char)cmd);
        break;
      case 3:
        fprintf(stderr, "CSI: Unknown arg1=%ld arg2=%ld arg3=%ld cmd=%c\n", arg[0], arg[1], arg[2], (char)cmd);
        break;
      default:
        fprintf(stderr, "CSI: Unknown arg1=%ld arg2=%ld arg3=%ld ... args=%d cmd=%c\n", arg[0], arg[1], arg[2], args, (char)cmd);
        break;
    }
#endif
    return TERMKEY_RES_NONE;
  }

  *nbytep = csi_end + 1;
  return result;
}

static TermKeyResult peekkey_ss3(TermKey *tk, TermKeyCsi *csi, size_t introlen, TermKeyKey *key, int force, size_t *nbytep)
{
  if(tk->buffcount < introlen + 1) {
    if(!force)
      return TERMKEY_RES_AGAIN;

    (*tk->method.emit_codepoint)(tk, 'O', key);
    key->modifiers |= TERMKEY_KEYMOD_ALT;
    *nbytep = tk->buffcount;
    return TERMKEY_RES_KEY;
  }

  unsigned char cmd = CHARAT(introlen);

  if(cmd < 0x40 || cmd >= 0x80)
    return TERMKEY_RES_NONE;

  key->type = csi_ss3s[cmd - 0x40].type;
  key->code.sym = csi_ss3s[cmd - 0x40].sym;
  key->modifiers = csi_ss3s[cmd - 0x40].modifier_set;

  if(key->code.sym == TERMKEY_SYM_UNKNOWN) {
    if(tk->flags & TERMKEY_FLAG_CONVERTKP && ss3_kpalts[cmd - 0x40]) {
      key->type = TERMKEY_TYPE_UNICODE;
      key->code.codepoint = ss3_kpalts[cmd - 0x40];
      key->modifiers = 0;

      key->utf8[0] = key->code.codepoint;
      key->utf8[1] = 0;
    }
    else {
      key->type = ss3s[cmd - 0x40].type;
      key->code.sym = ss3s[cmd - 0x40].sym;
      key->modifiers = ss3s[cmd - 0x40].modifier_set;
    }
  }

  if(key->code.sym == TERMKEY_SYM_UNKNOWN) {
#ifdef DEBUG
    fprintf(stderr, "CSI: Unknown SS3 %c (0x%02x)\n", (char)cmd, cmd);
#endif
    return TERMKEY_RES_NONE;
  }

  *nbytep = introlen + 1;

  return TERMKEY_RES_KEY;
}

static TermKeyResult peekkey(TermKey *tk, void *info, TermKeyKey *key, int force, size_t *nbytep)
{
  if(tk->buffcount == 0)
    return tk->is_closed ? TERMKEY_RES_EOF : TERMKEY_RES_NONE;

  TermKeyCsi *csi = info;

  // Now we're sure at least 1 byte is valid
  unsigned char b0 = CHARAT(0);

  if(b0 == 0x1b && tk->buffcount > 1 && CHARAT(1) == '[') {
    return peekkey_csi(tk, csi, 2, key, force, nbytep);
  }
  else if(b0 == 0x1b && tk->buffcount > 1 && CHARAT(1) == 'O') {
    return peekkey_ss3(tk, csi, 2, key, force, nbytep);
  }
  else if(b0 == 0x8f) {
    return peekkey_ss3(tk, csi, 1, key, force, nbytep);
  }
  else if(b0 == 0x9b) {
    return peekkey_csi(tk, csi, 1, key, force, nbytep);
  }
  else
    return TERMKEY_RES_NONE;
}

struct TermKeyDriver termkey_driver_csi = {
  .name        = "CSI",

  .new_driver  = new_driver,
  .free_driver = free_driver,

  .peekkey = peekkey,
};
