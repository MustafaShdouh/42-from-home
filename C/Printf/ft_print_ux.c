/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_ux.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/18 22:24:55 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/18 22:31:47 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_print_unsigned(unsigned int n)
{
	int	len;

	len = 0;
	if (n >= 10)
		len += ft_print_unsigned(n / 10);
	len += ft_print_char((n % 10) + '0');
	return (len);
}

int	ft_print_hex(unsigned int num, const char format)
{
	int	len;

	len = 0;
	if (num >= 16)
		len += ft_print_hex(num / 16, format);
	if (format == 'x')
		len += ft_print_char("0123456789abcdef"[num % 16]);
	if (format == 'X')
		len += ft_print_char("0123456789ABCDEF"[num % 16]);
	return (len);
}
