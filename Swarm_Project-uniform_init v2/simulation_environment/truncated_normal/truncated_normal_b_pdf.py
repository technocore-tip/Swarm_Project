#! /usr/bin/env python
#
def truncated_normal_b_pdf ( x, mu, sigma, b ):

#*****************************************************************************80
#
## TRUNCATED_NORMAL_B_PDF evaluates the upper Truncated Normal PDF.
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    24 January 2017
#
#  Author:
#
#    John Burkardt
#
#  Parameters:
#
#    Input, real X, the argument of the PDF.
#
#    Input, real MU, SIGMA, the mean and standard deviation of the
#    parent Normal distribution.
#
#    Input, real B, the upper truncation limit.
#
#    Output, real VALUE, the value of the PDF.
# 
  from normal_01_cdf import normal_01_cdf
  from normal_01_pdf import normal_01_pdf

  if ( x <= b ):
  
    beta = ( b - mu ) / sigma
    xi = ( x - mu ) / sigma

    alpha_cdf = 0.0
    beta_cdf = normal_01_cdf ( beta )
    xi_pdf = normal_01_pdf ( xi )

    value = xi_pdf / ( beta_cdf - alpha_cdf ) / sigma

  else:
  
    value = 0.0
    
  return value

def truncated_normal_b_pdf_test ( ):

#*****************************************************************************80
#
## TRUNCATED_NORMAL_B_PDF_TEST tests TRUNCATED_NORMAL_B_PDF.
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    09 March 2015
#
#  Author:
#
#    John Burkardt
#
  import platform
  from truncated_normal_b_pdf_values import truncated_normal_b_pdf_values

  print ( '' )
  print ( 'TRUNCATED_NORMAL_B_PDF_TEST' )
  print ( '  Python version: %s' % ( platform.python_version ( ) ) )
  print ( '  TRUNCATED_NORMAL_B_PDF evaluates the PDF' )
  print ( '  of the upper Truncated Normal distribution.' )
  print ( '' )
  print ( '  The "parent" normal distribution has' )
  print ( '    mean = mu' )
  print ( '    standard deviation = sigma' )
  print ( '  The parent distribution is truncated to' )
  print ( '  the interval (-oo,b]' )

  print ( '' )
  print ( '                                                 Stored         Computed' )
  print ( '       X        Mu         S         B             PDF             PDF' )
  print ( '' )

  n_data = 0

  while ( True ):

    n_data, mu, sigma, b, x, pdf1 = truncated_normal_b_pdf_values ( n_data )

    if ( n_data == 0 ):
      break

    pdf2 = truncated_normal_b_pdf ( x, mu, sigma, b )

    print ( '  %8.1f  %8.1f  %8.1f  %8.1f  %14g  %14g' \
      % ( x, mu, sigma, b, pdf1, pdf2 ) )
#
#  Terminate.
#
  print ( '' )
  print ( 'TRUNCATED_NORMAL_AB_PDF_TEST:' )
  print ( '  Normal end of execution.' )
  return

if ( __name__ == '__main__' ):
  from timestamp import timestamp
  timestamp ( )
  truncated_normal_b_pdf_test ( )
  timestamp ( )

